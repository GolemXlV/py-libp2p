"""Unit tests for basic Circuit Relay v2 protobuf messages and resource logic."""

from libp2p.relay.circuit_v2.pb import circuit_pb2 as proto
from libp2p.relay.circuit_v2.resources import RelayLimits, RelayResourceManager
from libp2p.peer.id import ID


def test_hop_message_roundtrip():
    msg = proto.HopMessage(
        type=proto.HopMessage.RESERVE,
        peer=proto.Peer(id=b"peer"),
        reservation=proto.Reservation(expire=10, addrs=[b"/ip4/1.1.1.1"], voucher=b"v"),
        limit=proto.Limit(duration=1, data=2),
    )
    data = msg.SerializeToString()
    msg2 = proto.HopMessage()
    msg2.ParseFromString(data)
    assert msg2.type == proto.HopMessage.RESERVE
    assert msg2.peer.id == b"peer"
    assert msg2.reservation.expire == 10
    assert msg2.limit.duration == 1


def test_reservation_manager_basic():
    limits = RelayLimits(duration=60, data=100, max_circuit_conns=2, max_reservations=1)
    mgr = RelayResourceManager(limits)
    peer = ID(b"peerid")
    assert mgr.can_accept_reservation(peer)
    ttl = mgr.reserve(peer)
    assert ttl == 60
    assert not mgr.can_accept_reservation(ID(b"other"))

