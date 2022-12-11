#!/usr/bin/env python3

import sys
import json
import random
from argparse import ArgumentParser

tournament_points = 0


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-2x",
        "--double-chance",
        action="store_true",
        default=False,
        help="indicate a 2x event is going on",
    )
    parser.add_argument(
        "-ms",
        "--mystery-shards",
        type=int,
        default=0,
        help="amount of mystery shards to open",
    )
    parser.add_argument(
        "-as",
        "--ancient-shards",
        type=int,
        default=0,
        help="amount of ancient shards to open",
    )
    parser.add_argument(
        "-vs",
        "--void-shards",
        type=int,
        default=0,
        help="amount of void shards to open",
    )
    parser.add_argument(
        "-ss",
        "--sacred-shards",
        type=int,
        default=0,
        help="amount of sacred shards to open",
    )
    return parser.parse_args(args=None if sys.argv[1:] else ["--help"])


class Shard:
    roll_map = {
        0: "Legendary",
        1: "Epic",
        2: "Rare",
        3: "Uncommon",
        4: "Common",
        5: "Undefined",  # Something unexpected happened.
    }

    roll_results = {
        "Legendary": 0,
        "Epic": 0,
        "Rare": 0,
        "Common": 0,
        "Uncommon": 0,
    }

    tounament_points_map = [500, 250, 10, 1, 1]  # Legendary -> Common awarded points

    # These get overridden
    rates = []
    mercy_rates = []
    mercy_counter = []

    def __repr__(self):
        return self.__class__.__name__

    @property
    def name(self):
        return self.__repr__()

    @property
    def can_2x(self):
        return self.name != "MysteryShard"

    @staticmethod
    def roll():
        return random.randint(1, 1000)

    def summon(self, is_2x=False) -> int:
        """base logic for simulating a single summon"""
        res = self.roll()
        for idx, rate in enumerate(self.rates):
            min_res, max_res = rate
            max_res = (max_res * 2) if self.can_2x and is_2x else max_res
            max_res += self.calc_mercy(idx)
            if min_res <= res and max_res >= res:
                self.reset_mercy(idx)
                return idx
        return 5  # Make the linter shut up.

    def bulk_summon(self, iterations=10, is_2x=False) -> list[int]:
        return [self.summon(is_2x) for _ in range(iterations)]

    def has_mercy(self, idx) -> bool:
        min_count, _ = self.mercy_rates[idx]
        return self.mercy_counter[idx] > min_count

    def calc_mercy(self, idx) -> int:
        """calculates the mercy modifier to add to the RNG before doing a summon"""
        min_count, rate = self.mercy_rates[idx]
        mercy_count = self.mercy_counter[idx]
        if not self.has_mercy(idx):
            return 0
        return (mercy_count - min_count) * rate

    def load_mercy(self, fp="mercy.json") -> None:
        """populates the simulator with your provided mercy values"""
        with open(fp) as f:
            mercy_values = json.loads(f.read())
        for idx, key in enumerate(mercy_values[self.name]):
            self.mercy_counter[idx] = mercy_values[self.name][key]

    def reset_mercy(self, idx) -> None:
        self.mercy_counter[idx] = 0

    def reset_results(self) -> None:
        for key in self.roll_results:
            self.roll_results[key] = 0

    def save_results(self, indexes) -> dict[str, int]:
        for idx in indexes:
            self.roll_results[self.roll_map[idx]] += 1
            self.add_tournament_points(idx)
        return self.roll_results

    def add_tournament_points(self, idx):
        global tournament_points
        val = self.tounament_points_map[idx]
        tournament_points += val

    def display_results(self) -> None:
        print(f"{self.name} results:")
        for rarity, count in self.roll_results.items():
            if count > 0:
                print(f"\t {rarity}: {count}")

    def do_summons(self, count, is_2x=False) -> None:
        if count == 0:
            return
        self.load_mercy()
        summons = self.bulk_summon(count, is_2x)
        self.save_results(summons)
        self.display_results()
        self.reset_results()


class SacredShard(Shard):
    rates = [
        [1, 60],  # 6% for legendary
        [61, 1000],  # 94% for epic
    ]

    mercy_rates = [
        [12, 20],  # 12x until +2% for legendary
        [0, 0],  # 0x until +0% for epics
    ]

    mercy_counter = [0, 0]


class AncientShard(Shard):
    rates = [
        [1, 5],  # 0.5% for legendary
        [6, 80],  # 8% for epic
        [81, 1000],  # 91.5% for rare
    ]

    mercy_rates = [
        [200, 50],  # 200x until +5% for legendary per shard
        [20, 20],  # 20x until +2% for epics
        [0, 0],  # 0x until +0% for rare
    ]

    mercy_counter = [0, 0, 0]


class VoidShard(AncientShard):
    # The summoning rates are mathematically the same as Ancient Shards.
    tournament_points_map = [650, 350, 50, 1, 1]  # Legendary -> Common awarded points


class MysteryShard(Shard):
    rates = [
        [0, 0],  # 0% legendary
        [0, 0],  # 0% epic
        [987, 1000],  # 1.4% rare
        [743, 986],  # 24.4% uncommon
        [1, 742],  # 74.2% common
    ]

    mercy_rates = [
        [0, 0],  # no mercy
        [0, 0],  # no mercy
        [0, 0],  # no mercy
        [0, 0],  # no mercy
        [0, 0],  # no mercy
    ]

    mercy_counter = [0, 0, 0, 0, 0]


if __name__ == "__main__":
    args = parse_args()
    if args.double_chance:
        print("2X summoning rate\n")
    SacredShard().do_summons(args.sacred_shards, args.double_chance)
    AncientShard().do_summons(args.ancient_shards, args.double_chance)
    VoidShard().do_summons(args.void_shards, args.double_chance)
    MysteryShard().do_summons(args.mystery_shards, args.double_chance)
    print()
    print("Tournament Points Earned:", tournament_points)
