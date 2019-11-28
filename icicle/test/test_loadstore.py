from nmigen.back.pysim import Simulator
from nmigen.hdl.ast import Delay
from nmigen.test.utils import FHDLTestCase

from icicle.loadstore import WordAlign, MemWidth, LoadStore


class WordAlignTestCase(FHDLTestCase):
    def test_word(self):
        m = WordAlign()
        with Simulator(m) as sim:
            def process():
                yield m.width.eq(MemWidth.WORD)
                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000000)
                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.wdata.eq(0x11223344)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1111)
                self.assertEqual((yield m.rdata), 0xAABBCCDD)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned), 0x11223344)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1111)
                self.assertEqual((yield m.rdata), 0x0A0B0C0D)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned), 0x11223344)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1111)
                self.assertEqual((yield m.rdata), 0xAABBCCDD)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned), 0x11223344)

                yield m.addr.eq(0x80000001)
                yield Delay()
                self.assertEqual((yield m.misaligned), 1)

                yield m.addr.eq(0x80000002)
                yield Delay()
                self.assertEqual((yield m.misaligned), 1)

                yield m.addr.eq(0x80000003)
                yield Delay()
                self.assertEqual((yield m.misaligned), 1)
            sim.add_process(process)
            sim.run()

    def test_half(self):
        m = WordAlign()
        with Simulator(m) as sim:
            def process():
                yield m.width.eq(MemWidth.HALF)
                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000000)
                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.wdata.eq(0x11223344)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0011)
                self.assertEqual((yield m.rdata), 0xFFFFCCDD)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFFFF, 0x3344)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0011)
                self.assertEqual((yield m.rdata), 0x0C0D)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFFFF, 0x3344)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0011)
                self.assertEqual((yield m.rdata), 0xCCDD)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFFFF, 0x3344)

                yield m.addr.eq(0x80000001)
                yield Delay()
                self.assertEqual((yield m.misaligned), 1)

                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000002)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1100)
                self.assertEqual((yield m.rdata), 0xFFFFAABB)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFFFF0000, 0x33440000)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1100)
                self.assertEqual((yield m.rdata), 0x0A0B)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFFFF0000, 0x33440000)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1100)
                self.assertEqual((yield m.rdata), 0xAABB)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFFFF0000, 0x33440000)

                yield m.addr.eq(0x80000003)
                yield Delay()
                self.assertEqual((yield m.misaligned), 1)
            sim.add_process(process)
            sim.run()

    def test_byte(self):
        m = WordAlign()
        with Simulator(m) as sim:
            def process():
                yield m.width.eq(MemWidth.BYTE)
                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000000)
                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.wdata.eq(0x11223344)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0001)
                self.assertEqual((yield m.rdata), 0xFFFFFFDD)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF, 0x44)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0001)
                self.assertEqual((yield m.rdata), 0x0D)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF, 0x44)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0001)
                self.assertEqual((yield m.rdata), 0xDD)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF, 0x44)

                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000001)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0010)
                self.assertEqual((yield m.rdata), 0xFFFFFFCC)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF00, 0x4400)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0010)
                self.assertEqual((yield m.rdata), 0x0C)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF00, 0x4400)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0010)
                self.assertEqual((yield m.rdata), 0xCC)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF00, 0x4400)

                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000002)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0100)
                self.assertEqual((yield m.rdata), 0xFFFFFFBB)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF0000, 0x440000)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0100)
                self.assertEqual((yield m.rdata), 0x0B)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF0000, 0x440000)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b0100)
                self.assertEqual((yield m.rdata), 0xBB)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF0000, 0x440000)

                yield m.unsigned.eq(0)
                yield m.addr.eq(0x80000003)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1000)
                self.assertEqual((yield m.rdata), 0xFFFFFFAA)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF000000, 0x44000000)

                yield m.rdata_aligned.eq(0x0A0B0C0D)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1000)
                self.assertEqual((yield m.rdata), 0x0A)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF000000, 0x44000000)

                yield m.rdata_aligned.eq(0xAABBCCDD)
                yield m.unsigned.eq(1)
                yield Delay()
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.mask), 0b1000)
                self.assertEqual((yield m.rdata), 0xAA)
                self.assertEqual((yield m.addr_aligned), 0x80000000)
                self.assertEqual((yield m.wdata_aligned) & 0xFF000000, 0x44000000)
            sim.add_process(process)
            sim.run()


class LoadStoreTestCase(FHDLTestCase):
    def test_load(self):
        m = LoadStore()
        with Simulator(m) as sim:
            def process():
                self.assertEqual((yield m.busy), 0)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.bus.cyc), 0)

                yield m.valid.eq(1)
                yield m.load.eq(1)
                yield m.width.eq(MemWidth.WORD)
                yield m.addr.eq(0x11223344)
                yield Delay()

                self.assertEqual((yield m.busy), 1)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.bus.cyc), 1)
                self.assertEqual((yield m.bus.stb), 1)
                self.assertEqual((yield m.bus.we), 0)
                self.assertEqual((yield m.bus.adr), 0x11223344 >> 2)

                yield m.bus.ack.eq(1)
                yield m.bus.dat_r.eq(0xAABBCCDD)
                yield Delay()

                self.assertEqual((yield m.busy), 0)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.rdata), 0xAABBCCDD)

                yield m.valid.eq(0)
                yield Delay()

                self.assertEqual((yield m.busy), 0)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.bus.cyc), 0)
            sim.add_process(process)
            sim.run()

    def test_store(self):
        m = LoadStore()
        with Simulator(m) as sim:
            def process():
                self.assertEqual((yield m.busy), 0)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.bus.cyc), 0)

                yield m.valid.eq(1)
                yield m.store.eq(1)
                yield m.width.eq(MemWidth.WORD)
                yield m.addr.eq(0x11223344)
                yield m.wdata.eq(0xAABBCCDD)
                yield Delay()

                self.assertEqual((yield m.busy), 1)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.bus.cyc), 1)
                self.assertEqual((yield m.bus.stb), 1)
                self.assertEqual((yield m.bus.we), 1)
                self.assertEqual((yield m.bus.adr), 0x11223344 >> 2)
                self.assertEqual((yield m.bus.dat_w), 0xAABBCCDD)

                yield m.bus.ack.eq(1)
                yield Delay()

                self.assertEqual((yield m.busy), 0)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)

                yield m.valid.eq(0)
                yield Delay()

                self.assertEqual((yield m.busy), 0)
                self.assertEqual((yield m.misaligned), 0)
                self.assertEqual((yield m.fault), 0)
                self.assertEqual((yield m.bus.cyc), 0)
            sim.add_process(process)
            sim.run()
