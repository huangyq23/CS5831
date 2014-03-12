#!/usr/bin/env python

import random

class Tree:
    next_address = 0
    def __init__(self, bucket_size):
        self.bucket_size = bucket_size
        self.bucket = []
        self.left_child = None
        self.right_child = None
        self.address = Tree.next_address
        Tree.next_address += 1


def build_tree(depth, bucket_size):
    root = Tree(bucket_size)
    leaves = [root]
    for _ in range(depth):
        new_leaves = []
        for node in leaves:
            node.left_child = Tree(bucket_size)
            node.right_child = Tree(bucket_size)
            new_leaves.append(node.left_child)
            new_leaves.append(node.right_child)
        leaves = new_leaves
    return root

class ORAM:
    def __init__(self, bucket_size, tree_depth, secure_mem_size=1000000, unsecure_mem_size=100000000, word_size=4):
        secure_mem_size = secure_mem_size / word_size
        unsecure_mem_size = unsecure_mem_size / word_size
        self.tree_depth = tree_depth
        self.num_blocks = bucket_size * (2 ** (tree_depth + 1))
        self.block_size = unsecure_mem_size / self.num_blocks
        self.map_size = (8 * secure_mem_size / tree_depth)
        self.position_map = [None] * self.map_size
        self.tree = build_tree(tree_depth, bucket_size)

    def process_input(self, memory_addresses):
        for addr in memory_addresses:
            self.process_memory_access(int(addr))
    
    def access_path(self, path):
        node = self.tree
        current_mem_addr = ''
        for bit in path:
            if bit == '0':
                node = node.left_child
            if bit == '1':
                node = node.right_child
            current_mem_addr += bit
            print "{0}".format(node.address)

    def flush(self):
        self.access_path(self.gen_path())

    def gen_path(self):
        num_path = random.getrandbits(self.tree_depth)
        path = "{0:b}".format(num_path)
        path = path.zfill(self.tree_depth)
        return path

    def fetch(self, addr):
        block = addr / self.block_size
        path = self.position_map[block]
        if path == None:
            path = self.gen_path()
        self.access_path(path)

    def update_pos_map(self, addr):
        block = addr / self.block_size
        self.position_map[block] = self.gen_path()

    def put_back(self):
        pass 

    def process_memory_access(self, addr):
        self.fetch(addr)
        self.update_pos_map(addr)
        self.put_back()
        self.flush()

def gen_addr_accesses(n, m):
    addrs = range(n)
    addr_accesses = []
    for _ in range(m):
        addr_accesses.append(random.choice(addrs))
    return addr_accesses

def generate_memory_access_pattern():
    addrs = gen_addr_accesses(200, 10000)
    for addr in addrs:
        print str(addr)

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) == 0:
        generate_memory_access_pattern()
    else:
        file_name = args[0]
        with open(file_name) as mem_input:
            oram = ORAM(5, 15)
            oram.process_input(mem_input)
    
