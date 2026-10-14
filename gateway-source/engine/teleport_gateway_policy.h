/* SPDX-License-Identifier: GPL-2.0-only */
/** Independent, deterministic gateway pairing policy. No train relocation. */
#ifndef TELEPORT_GATEWAY_POLICY_H
#define TELEPORT_GATEWAY_POLICY_H
#include <algorithm>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <vector>
namespace TeleportGateway {
constexpr uint16_t UNPAIRED = 0xFFFF;
struct Endpoint {
    uint16_t id;
    uint8_t owner;
    uint64_t sequence;
    uint16_t partner;
    uint64_t partner_sequence;
};
/** Preserve reciprocal same-owner links, then pair oldest waiting endpoints. */
inline void Reconcile(std::vector<Endpoint> &endpoints)
{
    std::sort(endpoints.begin(), endpoints.end(), [](const auto &a, const auto &b) { return a.id < b.id; });
    uint64_t next = 0;
    for (const auto &e : endpoints) next = std::max(next, e.sequence);
    auto find = [&](uint16_t id) -> Endpoint * {
        auto it = std::lower_bound(endpoints.begin(), endpoints.end(), id,
            [](const auto &e, uint16_t id) { return e.id < id; });
        return it != endpoints.end() && it->id == id ? &*it : nullptr;
    };
    // Validate all links against the original state before mutating either end.
    std::vector<bool> valid(endpoints.size());
    for (size_t i = 0; i < endpoints.size(); ++i) {
        const auto &e = endpoints[i];
        const auto *p = find(e.partner);
        valid[i] = e.sequence != 0 && p != nullptr && p != &e && p->sequence != 0 &&
            p->owner == e.owner && p->partner == e.id && e.partner_sequence == p->sequence &&
            p->partner_sequence == e.sequence;
    }
    for (size_t i = 0; i < endpoints.size(); ++i) {
        auto &e = endpoints[i];
        if (!valid[i]) { e.partner = UNPAIRED; e.partner_sequence = 0; }
        if (e.sequence == 0) {
            if (next == std::numeric_limits<uint64_t>::max()) throw std::overflow_error("Gateway creation sequence exhausted");
            e.sequence = ++next;
        }
    }
    std::vector<Endpoint *> waiting;
    for (auto &e : endpoints) if (e.partner == UNPAIRED) waiting.push_back(&e);
    std::sort(waiting.begin(), waiting.end(), [](const auto *a, const auto *b) {
        return a->sequence != b->sequence ? a->sequence < b->sequence : a->id < b->id;
    });
    // Owner buckets prevent links between independent companies.
    Endpoint *first[256]{};
    for (auto *e : waiting) {
        auto *&p = first[e->owner];
        if (p == nullptr) { p = e; continue; }
        p->partner = e->id; p->partner_sequence = e->sequence;
        e->partner = p->id; e->partner_sequence = p->sequence;
        p = nullptr;
    }
}
} // namespace TeleportGateway
#endif
