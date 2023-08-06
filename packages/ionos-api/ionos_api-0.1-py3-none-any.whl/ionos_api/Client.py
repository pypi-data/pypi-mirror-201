from typing import Iterable, Set
from dataclasses import asdict

from .HTTPSession import HTTPSession
from .Model import Zone, Record, RecordDefinition


def parent_domain(domain: str, level: int):
    return ".".join((domain.split('.')[-level:]))


class Client(object):
    def __init__(self, url, full_key):
        s_headers = {"X-API-Key": full_key}
        self.session = HTTPSession(base_path=url, common_headers=s_headers)

    def zones(self) -> Iterable[Zone]:
        for d in self.session.get("/zones"):
            yield Zone(**d)

    def zone_for_domain(self, domain: str) -> Zone:
        master_domain = parent_domain(domain, 2)
        matching = list(filter(lambda z: z.name == master_domain, self.zones()))

        if len(matching) == 0:
            raise KeyError(domain)
        if len(matching) > 1:
            raise RuntimeError("More than one zone matching the master domain \"%s\"" % master_domain)

        return matching[0]

    def records_for_zone(self, zone: Zone) -> Iterable[Record]:
        print("/zones/" + zone.id)
        req_res = self.session.get("/zones/" + zone.id)
        if "records" in req_res:
            for d in req_res["records"]:
                yield Record(**d)

    def records_for_domain_in_zone(self, zone: Zone, domain: str, r_types: Set[str] = None):
        for r in self.records_for_zone(zone):
            if r.name == domain:
                if r_types is None or r.type in r_types:
                    yield r

    def records_for_domain(self, domain, r_types=None):
        zone = self.zone_for_domain(domain)
        return list(self.records_for_domain_in_zone(zone, domain, r_types))

    def add_record_to_zone(self, zone: Zone, record_definition: RecordDefinition):
        if any(r == record_definition for r in self.records_for_zone(zone)):
            raise ValueError("Record already exists.")
        res = self.session.post("/zones/" + zone.id + "/records",
                                body=[{k: v for k, v in asdict(record_definition).items() if v is not None}])
        return res

    def remove_record_from_zone(self, zone: Zone, record_definition: RecordDefinition):
        found = list(filter(lambda r: r == record_definition, self.records_for_zone(zone)))
        if len(found) == 0:
            raise KeyError(record_definition)

        for r in found:
            self.session.delete("/zones/" + zone.id + "/records/" + r.id)

    def add_record(self, record_definition: RecordDefinition):
        zone = self.zone_for_domain(record_definition.name)
        return self.add_record_to_zone(zone, record_definition)

    def remove_record(self, record_definition: RecordDefinition):
        zone = self.zone_for_domain(record_definition.name)
        self.remove_record_from_zone(zone, record_definition)
