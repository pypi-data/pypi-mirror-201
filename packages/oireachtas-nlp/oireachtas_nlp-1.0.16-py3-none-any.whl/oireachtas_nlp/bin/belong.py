import argparse
import multiprocessing
from collections import defaultdict, Counter

import tqdm

from gensim.models import Doc2Vec

from oireachtas_data import members

from oireachtas_nlp import logger
from oireachtas_nlp.learn.tags import MemberTaggedDocs, PartyTaggedDocs
from oireachtas_nlp.learn.classifier import ClassifierCreator


def get_percentages(d):
    s = sum(d.values())
    res = {}
    for k, v in d.items():
        pct = v * 100.0 / s
        res[k] = pct
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", dest="epochs", type=int, default=25)
    parser.add_argument(
        "--min-per-member-group", dest="min_per_member_group", type=int, default=150
    )
    parser.add_argument(
        "--max-per-member-group", dest="max_per_member_group", type=int, default=150
    )
    parser.add_argument(
        "--min-per-party-group", dest="min_per_party_group", type=int, default=3000
    )
    parser.add_argument(
        "--max-per-party-group", dest="max_per_party_group", type=int, default=7500
    )
    parser.add_argument(
        "--doc2vec-minword", dest="doc2vec_minword", type=int, default=5
    )
    parser.add_argument("--window", dest="window", type=int, default=10)
    parser.add_argument("--vector-size", dest="vector_size", type=int, default=250)
    parser.add_argument("--negative", dest="negative", type=int, default=10)
    parser.add_argument(
        "--workers", dest="workers", type=int, default=multiprocessing.cpu_count() - 1
    )
    parser.add_argument("--train-ratio", dest="train_ratio", type=int, default=0.8)

    members.load()

    parser.add_argument(
        "--member-pid",
        dest="member_pid",
        type=str,
        choices=set([d.pid for d in members.data if d.pid]),
        default=None,
    )

    args = parser.parse_args()

    if not args.member_pid:
        logger.warning(
            "--member-pid is not specified so each member will likely have some data included in the train set for the party. The paragraphs used in testing the association with a party will not be included in the party training data"
        )

    member_tagged_docs = MemberTaggedDocs(
        min_per_group=args.min_per_member_group,
        max_per_group=args.max_per_member_group,
        only_member_pids=[args.member_pid] if args.member_pid else [],
    )
    member_tagged_docs.load_tagged_docs()
    member_tagged_docs.clean_data()

    if len(member_tagged_docs) == 0:
        raise Exception(
            "Not enough member data, load more debates or lower member thresholds"
        )
    else:
        logger.info(f"Member tagged docs: {len(member_tagged_docs)}")

    party_tagged_docs = PartyTaggedDocs(
        min_per_group=args.min_per_party_group,
        max_per_group=args.max_per_party_group,
        exclude_para_hashes=member_tagged_docs.get_para_hashes(),  # Don't allow paras we will be predicting to be in training
        exclude_member_pids=[args.member_pid] if args.member_pid else [],
    )
    party_tagged_docs.load_tagged_docs()
    party_tagged_docs.clean_data()

    if len(party_tagged_docs) == 0:
        raise Exception(
            "Not enough party data, load more debates or lower member thresholds"
        )
    else:
        logger.info(f"Party tagged docs: {len(party_tagged_docs)}")

    # FIXME: Seems to do bad for when lots of people

    party_classifier_creator = ClassifierCreator(
        Doc2Vec(
            min_count=args.doc2vec_minword,
            window=args.window,
            vector_size=args.vector_size,
            sample=1e-4,
            negative=args.negative,
            workers=args.workers,
        ),
        party_tagged_docs,
        equalize_group_contents=True,
        train_ratio=args.train_ratio,
        epochs=args.epochs,
    )

    logger.info("Generating party classifier")
    party_classifier_creator.generate_classifier()
    logger.info("Finished generating party classifier")

    # TODO: iter for each person and give results as we get them rather than processing them all
    logger.info("Generating individual member results")
    member_results = defaultdict(lambda: defaultdict(int))
    for member_para_tuple in tqdm.tqdm(member_tagged_docs.items):
        member = member_para_tuple[0]
        paras = member_para_tuple[1]
        content = "\n\n".join([p.content for p in paras])
        result, score = party_classifier_creator.predict(content)
        member_results[member][result] += 1
    logger.info("Finished generating individual member results")

    potential_parties = set()
    for results in member_results.values():
        potential_parties = potential_parties.union(
            [i.replace("_", "") for i in list(results.keys())]
        )

    for member, results in member_results.items():
        parties = members.parties_of_member(member)
        if parties is None:
            continue
        if len(parties) > 1:
            continue
        if parties[0].replace("_", "") not in potential_parties:
            continue

        percs = get_percentages(results)

        most_likely = Counter(percs).most_common()[0][0]
        percentages = {
            k: round(v, 2)
            for k, v in dict(
                sorted(percs.items(), key=lambda x: x[1], reverse=True)
            ).items()
        }

        # FIXME: ugly
        actual = parties[0].replace("_", "")

        if most_likely != actual:
            logger.warning(
                f"{member} looks like they belong to {most_likely} but actually belong to {actual}. Confidence: {percentages}"
            )
        else:
            logger.info(f"{member} belongs to {actual}. Confidence: {percentages}")


if __name__ == "__main__":
    main()
