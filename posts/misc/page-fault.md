---
title: Page fault
date: 2021/11/28
description: From virtual memory to how a page fault works
tags:
  - OS
  - memory
---

I recently reopened an old project of mine, and by reading my own code and comments I re-explored what a page fault is and wanted to write it down in here!

## Virtual address space

To understand a page fault, it's necessary to understand how the memory is organized first.

### Process memory

When multiple processes run at the same time, we need to ensure they are isolated from one another. We don't want a process A being able to read or write a memory value from process B.

These addresses also need to be relative and not absolute.
Imagine process A requests 4096 bytes so it could use `0x0000` to `0x0fff` and process B needs 8192 bytes so from `0x1000` to `0x2fff`.
Now process A terminates and process C requests 8092 bytes but it can't fit in process A old space so we now have a tiny gap and we just created memory fragmentation.
At some point we may run out of memory.

To deal with these issues, each process has its own address space which depends on the architecture (for ex: $2^{32}$ addresses for a 32-bit architecture)

*Notes*:

* The physical memory doesn't have to be as big as the address space.
* The OS reserves some of the virtual memory for itself.

### Pages

When the CPU needs to access an address, the address is first sent to an MMU ([Memory Management Unit](https://en.wikipedia.org/wiki/Memory_management_unit)) which translates it to a physical address and then sends the address on the memory bus.

The virtual address space is split into fixed memory range called pages. The physical address space is also split into pages called page frames. Usually virtual pages and page frames are the same size.

This allows to load an entire contiguous range of memory instead of a single value.

The OS keeps a mapping between virtual page / page frame that it shares with the MMU in order to translate a virtual address into a physical address.
The MMU extracts from the address:

* a page index
* an offset

The MMU can then use the page index to retrieve the page frame from the page table and adds the offset back to get the physical address.

### Page table

### Page table entry

A page table entry contains more than just the page frame number:

<img src="/img/misc/page-fault/page_table_entry.jpg">

with:

* Present/Absent: If this bit is 0, it means the page isn't mapped (i.e. a page fault if it is accessed)
* Protection: It reflects the permission of the page, read/write or read only, etc. It can be 1 bit or 3 bits for more granular permissions.
* Modified: If a page is written (as being used), this bit is automatically set to 1. It allows the OS to decide if the page needs to be written to disk or if it's still clean since the last save.
* Referenced: Sets if a page is referenced for writing or reading. It also helps the OS to decide on which page is less used.
* Caching disabled: Help to decide whether the cache for this page should be disabled.

### Mapping

For example: If there are 16 virtual pages to represent address from 0 to 65536. Each address could be made of 4 bits to represent the virtual page index and 12 bits for the offset, which gives us 4096 possible offsets so each page should be 4096. In this case, address 24976 (= 0x6190) can be seen as 4 bits, 0x6, for the virtual page number and 12 bits, 0x190 = 400, for the offset.

<img src="/img/misc/page-fault/virtual_mapping.jpg">

Now accessing address `24976` is at virtual page 6. Virtual page 6 starts at address 24576 ($4096 x 6$) and the address has an offset of 400 so the MMU translates it to page frame 3 with offset 400 so it becomes $8192 + 400 = 8592$

However, if you try accessing virtual address `28772` (virtual page 7), it's not mapped, in that case it causes the CPU to [trap](https://en.wikipedia.org/wiki/Trap_(computing)) the OS, which is called a **page-fault**.

## Page-fault management

When the OS receives a page-fault from the CPU, it needs to remap the virtual page to a page-frame.
It selects a virtual page that is less used (using the Modified and Referenced bits), saves the physical page, retrieves the referenced page (previously unmapped) and loads it into the page frame.
Finally, it updates the page table and restarts the CPU instruction that traps.

There are 2 types of page-fault:

* soft: the page can be retrieved from memory cache
* hard: the page needs to be copied from disk (much slower)
