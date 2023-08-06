from dataclasses import dataclass


@dataclass
class KBIteratorConfig:
    max_total_count: int
    earliest_created_time: int
