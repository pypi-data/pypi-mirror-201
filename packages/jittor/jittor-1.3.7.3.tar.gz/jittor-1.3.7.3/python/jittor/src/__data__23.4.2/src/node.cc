// ***************************************************************
// Copyright (c) 2020 Jittor. Authors: Dun Liang <randonlang@gmail.com>. All Rights Reserved.
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#include "pybind/py_var_tracer.h"
#include "mem/allocator.h"
#include "node.h"
#include "op.h"
#include "var.h"

namespace jittor {


int64 tflag_count = 0;
int64 nt = 0;

unordered_map<void*, int64> lived_nodes;
unordered_map<int64, Node*> lived_nodes_id;
int64 total_node = 0;
vector<Node*> free_buffer;
extern void free_var(Var* v);
extern void free_var_mem(Var* v);

void Node::free() {
    CHECK_EXIST;
    if (tflag == nt)
        return;
    // var can only be freed by backward_liveness
    // if var's input op is not freed, we need to keep it
    if (is_var() && _inputs.size() && (forward_liveness || !is_finished())) {
        return;
    }
    tflag = nt;
    free_buffer.push_back(this);
    // release input
    for (auto i : _inputs) {
        i.node->_outputs.erase(i.back);
            if (backward_liveness) {
                i.node->release_backward_liveness();
            }
            if (pending_liveness && !is_finished())
                i.node->release_pending_liveness();
    }
    _inputs.clear();
    // release output
    for (auto o : _outputs) {
        o.node->_inputs.erase(o.back);
        if (!is_stop_grad()) {
            if (forward_liveness)
                o.node->release_forward_liveness();
        }
        #ifdef JT_haha2
        if (o.node->is_var() && o.node->need_free())
            o.node->free();
        #else
        if (o.node->is_var() && o.node->backward_liveness==0)
            o.node->free();
        #endif
    }
    _outputs.clear();
    if (is_var()) free_var((Var*)this);
}

void Node::__release() {
    if (is_var())
        Var::number_of_lived_vars--;
    else
        Op::number_of_lived_ops--;
    tflag = -1;
}

void Node::memcheck_all_exist() const {
#ifdef NODE_MEMCHECK
    CHECK_EXIST;
    for (auto& i : _inputs)
        CHECK_NODE_EXIST(i.node);
    for (auto& o : _outputs)
        CHECK_NODE_EXIST(o.node);
#endif
}

void Node::own_pending_liveness() {
    CHECK_EXIST;
    pending_liveness++;
    if (pending_liveness==1 && !is_finished())
        for (auto* i : inputs())
            i->own_pending_liveness();
}

void Node::release_pending_liveness() {
    CHECK_EXIST;
    pending_liveness--;
    if (!pending_liveness && !is_finished()) {
        // p2: output(p>0 and pending) contrib pending_liveness
        for (auto* i : inputs())
            i->release_pending_liveness();
    }
    if (pending_liveness == 0 && is_var() && ((Var*)this)->mem_ptr != nullptr && flags.get(NodeFlags::_needed_by_backward) == 0) {
        free_var_mem((Var*)this);
    }
}

void Node::release_forward_liveness() {
    CHECK_EXIST;
    forward_liveness--;
    if (!forward_liveness) {
        // f3. input(has_grad and f>0) contrib one forward_liveness
        int n = outputs().size(), i=0;
        STACK_ALLOC(Node*,os,n);
        for (auto* o : outputs()) {
            os[i++] = o;
        }
        if (!is_stop_grad()) {
            for (int i=0; i<n; i++) {
                auto o = os[i];
                o->release_forward_liveness();
            }
        }
        if (backward_liveness) {
            for (int i=0; i<n; i++) {
                auto o = os[i];
                if (o->is_var() && o->is_finished()) {
                    if (o->is_stop_grad()) continue;
                    release_backward_liveness();
                }
            }
        }
    }
}

void Node::own_forward_liveness() {
    CHECK_EXIST;
    forward_liveness++;
    if (forward_liveness==1) {
        // f2. input(has_grad and f>0) contrib one forward_liveness
        if (!is_stop_grad())
            for (auto* o : outputs())
                o->own_forward_liveness();
        #ifdef JT_haha
        // p1: pending and f>0 and b>0 contrib pending_liveness
        if (backward_liveness && !is_finished())
            own_pending_liveness();
        #endif
    }
}

void Node::release_backward_liveness() {
    CHECK_EXIST;
    backward_liveness--;
    if (!backward_liveness) {
        #ifdef JT_haha
        // p1: pending and f>0 and b>0 contrib pending_liveness
        if (forward_liveness && !is_finished())
            release_pending_liveness();
        #endif
        // b3. output(b>0) contrib one backward_liveness
        int n = inputs().size(), m=0;
        STACK_ALLOC(Node*,is,n);
        for (auto* i : inputs()) {
            is[m++] = i;
        }
        for (int j=0; j<n; j++) {
            auto i = is[j];
            if (i->forward_liveness==0 && is_finished() && is_var())
                // already released by other func
                continue;
            if (is_finished() && is_stop_grad())
                continue;
            i->release_backward_liveness();
        }
        LOGvvvv << "Free backward_liveness=0" << this;
        free();
    }
}

void Node::own_backward_liveness() {
    CHECK_EXIST;
    backward_liveness++;
    if (backward_liveness==1) {
        // b3. output(b>0) contrib one backward_liveness
        if (!is_finished() || !is_stop_grad())
            for (auto* i : inputs()) {
                i->own_backward_liveness();
            }
    }
}

void Node::own_both_liveness() {
    CHECK_EXIST;
    own_forward_liveness();
    own_backward_liveness();
    own_pending_liveness();
}

void Node::release_both_liveness() {
    CHECK_EXIST;
    SetupFreeBuffer setup_free_buffer;
    release_forward_liveness();
    release_backward_liveness();
    release_pending_liveness();
}

void Node::finish_pending_liveness() {
    CHECK_EXIST;
    if (is_finished()) return;
    SetupFreeBuffer setup_free_buffer;
    flags.set(NodeFlags::_finished);
    auto need_release = forward_liveness && backward_liveness;
    // p2: output(p>0 and pending) contrib pending_liveness
    if (pending_liveness)
        for (auto* i : inputs()) {
            i->release_pending_liveness();
        }
    if (is_var() || is_stop_grad()) {
            int n = inputs().size(), m=0;
            STACK_ALLOC(Node*,is,n);
            for (auto* i : inputs()) {
                is[m++] = i;
            }
            for (int j=0; j<n; j++) {
                auto i = is[j];
                if (i->forward_liveness == 0 || is_stop_grad()) {
                    i->release_backward_liveness();
                }
            }
    }
}

void Node::release_inputs() {
    CHECK_EXIST;
    if (!_inputs.size()) return;
    SetupFreeBuffer setup_free_buffer;
    for (auto i : _inputs) {
        if (!i.node->is_stop_grad() && i.node->forward_liveness)
            release_forward_liveness();
        i.node->_outputs.erase(i.back);
        if (backward_liveness) {
            i.node->release_backward_liveness();
        }
        if (pending_liveness)
            i.node->release_pending_liveness();
    }
    _inputs.clear();
}

void Node::set_inputs(list<Node*> nodes) {
    CHECK_EXIST;
    LOGvvvv << "Set inputs of" << this << "to" << nodes;
    ASSERT(!is_finished());
    // f2. input(has_grad and f>0) contrib one forward_liveness
    for (Node* node : nodes) {
        if (!node->is_stop_grad() && node->forward_liveness)
            own_forward_liveness();
        // we own liveness before release inputs
        // to prevent node be freed
        // b3. output(b>0) contrib one backward_liveness
        if (backward_liveness) {
            node->own_backward_liveness();
        }
        if (pending_liveness)
            node->own_pending_liveness();
    }
    release_inputs();
    bool is_var = this->is_var();
    auto inputs_iter = nodes.begin();
    for (size_t i=0; i<nodes.size(); i++, inputs_iter++) {
        Node* in = *inputs_iter;
        _inputs.emplace_back(in);
        in->_outputs.emplace_back(this, is_var?in->_outputs.size():i);
        _inputs.back().back = std::prev(in->_outputs.end());
        in->_outputs.back().back = std::prev(_inputs.end());
    }
}

// copy from set_inputs, remove release_inputs
void Node::add_inputs(const vector<Node*>& nodes) {
    CHECK_EXIST;
    LOGvvvv << "add inputs" << nodes << "to" << this;
    ASSERT(!is_finished());
    // f1. each input(need grad) contrib one forward_liveness
    for (Node* node : nodes) {
        if (!node->is_stop_grad() && node->forward_liveness)
            own_forward_liveness();
        // we own liveness before release inputs
        // to prevent node be freed
        // b3. output(b>0) contrib one backward_liveness
        if (backward_liveness) {
            node->own_backward_liveness();
        }
        if (pending_liveness)
            node->own_pending_liveness();
    }
    bool is_var = this->is_var();
    auto inputs_iter = nodes.begin();
    uint psize = _inputs.size();
    for (size_t i=0; i<nodes.size(); i++, inputs_iter++) {
        Node* in = *inputs_iter;
        _inputs.emplace_back(in);
        in->_outputs.emplace_back(this, is_var?in->_outputs.size():i+psize);
        _inputs.back().back = std::prev(in->_outputs.end());
        in->_outputs.back().back = std::prev(_inputs.end());
    }
}

void Node::add_inputs(const vector<Var*>& nodes) {
    add_inputs((const vector<Node*>&)nodes);
}

void Node::set_stop_grad() {
    CHECK_EXIST;
    if (is_stop_grad()) return;
    SetupFreeBuffer setup_free_buffer;
    // can not set is_stop_grad from true to false
    flags.set(NodeFlags::_stop_grad, 1);
    // f3. input(has_grad and f>0) contrib one forward_liveness
    int bl = backward_liveness;
    if (forward_liveness)
        for (Node* o : outputs())
            o->release_forward_liveness();

    if (bl) {
        int n = inputs().size(), x=0;
        STACK_ALLOC(Node*,is,n);
        for (auto* i : inputs()) {
            is[x++] = i;
        }
        for (int x=0; x<n; x++) {
            auto i = is[x];
            if (i->forward_liveness==0 && is_var() && is_finished()) {
                continue;
            }
            if (!is_finished()) continue;
            i->release_backward_liveness();
        }
    }
}

std::ostream& operator<<(std::ostream& os, const Node* node) {
    return node->is_var() ?  os << (const Var*)node : os << (const Op*)node;
}
} // jittor