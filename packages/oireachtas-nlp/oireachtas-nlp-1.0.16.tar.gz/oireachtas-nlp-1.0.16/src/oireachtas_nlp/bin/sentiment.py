import argparse
import multiprocessing
import random
from multiprocessing import Pool

import tqdm

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from oireachtas_data import members

from oireachtas_nlp import logger
from oireachtas_nlp.utils import get_speaker_para_map, get_party_para_map, sample


sia = SentimentIntensityAnalyzer()


def get_sentiment(data):
    sample_size, item = data
    paras = sample(item[1], sample_size)
    return (
        item[0],
        sia.polarity_scores(
            "\n\n".join([p.content for p in paras])
        ),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--group-by",
        dest="group_by",
        type=str,
        required=True,
        choices=["member", "party"],
    )
    parser.add_argument(
        "--sort-by",
        dest="sort_by",
        type=str,
        required=True,
        choices=["neg", "pos", "neu"],
    )
    parser.add_argument(
        "--sample-size",
        dest="sample_size",
        type=int,
        default=2500,
        help='How many paragraph samples to take from each group'
    )
    args = parser.parse_args()

    try:
        nltk.data.find("sentiment")
    except LookupError:  # pragma: nocover
        nltk.download("vader_lexicon")

    if args.group_by == "member":
        data = {}
        for speaker, paras in get_speaker_para_map(only_groups=None).items():
            if len(paras) < 100:
                continue

            member = members.get_member_from_name(speaker)
            if member is None:
                continue

            data[speaker] = paras

    elif args.group_by == "party":
        data = get_party_para_map(only_groups=None)

    data = {k: v for k, v in data.items() if len(v) > 10}

    results = {}

    pool = Pool(processes=multiprocessing.cpu_count() - 1)
    for res in tqdm.tqdm(
        pool.imap_unordered(get_sentiment, [(args.sample_size, d) for d in data.items()]), total=len(data)
    ):
        results[res[0]] = res[1]

    sorted_key_results = sorted(
        results, key=lambda x: results[x][args.sort_by], reverse=True
    )

    for k in sorted_key_results:
        logger.info(f"{k.ljust(30)} {results[k]}")


if __name__ == "__main__":
    main()
