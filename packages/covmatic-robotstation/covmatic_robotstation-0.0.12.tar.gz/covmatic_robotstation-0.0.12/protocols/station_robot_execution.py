from covmatic_robotstation.robot_station import RobotStationABC, labware_loader, instrument_loader

class FakeStation(RobotStationABC):
    @labware_loader(0, "_fake_tipracks")
    def load_fake_tiprack(self):
        self._fake_tipracks = [self._ctx.load_labware('opentrons_96_filtertiprack_20ul', "1", '20ul filter tiprack')]

    @instrument_loader(0, "_fake_pipette")
    def load_fake_pipette(self):
        self._fake_pipette = self._ctx.load_instrument('p20_multi_gen2', 'left', tip_racks=self._fake_tipracks)

    def _tipracks(self) -> dict:
        return {"_fake_tipracks": "_fake_pipette"}

    def body(self):
        self.robot_pick_plate("SLOT1", "TESTPLATE")
        self.robot_drop_plate("SLOT2", "TESTPLATE")
        self.robot_trash_plate("SLOT1", "TRASHSLOT2", "TRASHPLATE")


metadata = {'apiLevel': '2.7'}
station = FakeStation(ot_name="OTTEST", num_samples=96)


def run(ctx):
    return station.run(ctx)


if __name__ == "__main__":
    FakeStation(ot_name="OT1", metadata={'apiLevel': '2.7'}).simulate()
