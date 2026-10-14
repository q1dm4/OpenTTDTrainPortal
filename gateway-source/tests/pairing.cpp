// SPDX-License-Identifier: GPL-2.0-only
#include "teleport_gateway_policy.h"
#include <cassert>
#include <iostream>
#include <random>
using namespace TeleportGateway;
Endpoint &at(std::vector<Endpoint> &v, uint16_t id) {
    for (auto &e:v) if(e.id==id) return e;
    std::abort();
}
void invariant(std::vector<Endpoint> &v) {
    for (const auto &e:v) {
        assert(e.sequence>0);
        if(e.partner==UNPAIRED) {assert(e.partner_sequence==0); continue;}
        const auto &p=at(v,e.partner);
        assert(p.partner==e.id && p.id!=e.id && p.owner==e.owner);
        assert(p.sequence==e.partner_sequence && e.sequence==p.partner_sequence);
    }
}
int main() {
    std::vector<Endpoint> v{{10,0,0,UNPAIRED,0}};
    Reconcile(v); assert(at(v,10).partner==UNPAIRED);
    v.push_back({2,0,0,UNPAIRED,0}); Reconcile(v);
    assert(at(v,10).partner==2 && at(v,2).partner==10); // Creation order, not ID order.
    v.push_back({7,0,0,UNPAIRED,0}); Reconcile(v); assert(at(v,7).partner==UNPAIRED);
    v.push_back({5,0,0,UNPAIRED,0}); Reconcile(v);
    assert(at(v,7).partner==5); invariant(v);
    auto restored=v; std::reverse(restored.begin(),restored.end()); Reconcile(restored);
    for(const auto &e:v) {const auto &r=at(restored,e.id);assert(e.partner==r.partner && e.sequence==r.sequence);}
    // Removing one endpoint cannot disturb an unrelated surviving pair.
    v.erase(std::remove_if(v.begin(),v.end(),[](const auto &e){return e.id==2;}),v.end());
    Reconcile(v); assert(at(v,10).partner==UNPAIRED && at(v,7).partner==5);
    // A reused station ID starts a new endpoint identity.
    v.push_back({2,0,0,UNPAIRED,0}); Reconcile(v); invariant(v);
    assert(at(v,10).partner==2);
    // Different companies never pair; same-company waiting gateways do.
    v.push_back({20,1,0,UNPAIRED,0}); v.push_back({21,2,0,UNPAIRED,0});
    Reconcile(v); assert(at(v,20).partner==UNPAIRED && at(v,21).partner==UNPAIRED);
    v.push_back({22,1,0,UNPAIRED,0}); Reconcile(v); assert(at(v,20).partner==22);
    // Corrupt one-sided, self, and stale generation links are repaired.
    at(v,10).partner=10; Reconcile(v); invariant(v);
    at(v,20).partner_sequence=999; Reconcile(v); invariant(v);
    at(v,20).owner=2; Reconcile(v); invariant(v);
    std::mt19937 rng(73);
    for (uint16_t id=30;id<530;++id) {
        if(!v.empty() && rng()%3==0) v.erase(v.begin()+rng()%v.size());
        v.push_back({id,static_cast<uint8_t>(rng()%8),0,UNPAIRED,0});
        std::shuffle(v.begin(),v.end(),rng); Reconcile(v); invariant(v);
    }
    std::cout << "PASS: creation ordering, multiple pairs, ownership, removal, ID reuse, stale links, reload ordering, 500 topology mutations\n";
}
