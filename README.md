sc55-mcudump-patches
--------------------


What is this?
-------------

The SC-55 firmware consists of a 32 KB ROM built into the MCU and an external firmware ROM. These patches rewrite the bulk dump implementation in the external firmware ROM to bulk dump the contents of the MCU internal ROM.


How to Use
----------

* Hardware Preparation
	1. Dump external firmware ROM as a binary file from your SC-55.
	2. Use the [bspatch](https://github.com/mendsley/bsdiff) utility to apply the patch file corresponding to the model and firmware version.
		* e.g. `bspatch original_sc-55_v121.bin modified_sc-55_v121.bin sc-55_v121_mod.bdf`
	3. Program the modified firmware binary to any writable ROM compatible with the original firmware ROM.
	4. Replace the original firmware ROM to the newly programmed ROM.
* MIDI Recording and Converting
	1. Connect your PC to both the MIDI In and MIDI Out terminals of the SC-55 using a MIDI interface such as UM-ONE mk2.
	2. Prepare for MIDI recording with some kind of software for real-time MIDI recording.
	3. Play [mcu_bulkdump_request.mid](./tools/mcu_bulkdump_request.mid) with some kind of MIDI file playback software.
		* The playback of this MIDI file sends the bulk dump request SysEx 8 times. The SC-55 sends a bulk dump message each time it receives one of those requests.
		* It takes a little over a minute for all SysEx transmission and reception to complete.
	4. Save all received bulk dump messages in one file.
		* You can save in ".txt" (hex text), ".syx" (raw binary), or ".mid" (Standard MIDI File) format.
	5. Use the [sysex2bin.py](./tools/sysex2bin.py) utility to convert bulk dump messages to a binary file.
		* e.g. `python sysex2bin.py bulkdump.mid sc-55_mcu.bin`


Patches
-------

| File Name                                                | Model and Version  | SHA-256 (Original external firmware ROM)                           |
|----------------------------------------------------------|--------------------|--------------------------------------------------------------------|
| [sc-55_v100_mod.bdf](./patches/sc-55_v100_mod.bdf)       | SC-55 Ver.1.00     | `014e2e21ea30de7a1e4f1cdea14dd9a719960535e257a9e40e98dbb1a5870226` |
| [sc-55_v110_mod.bdf](./patches/sc-55_v110_mod.bdf)       | SC-55 Ver.1.10     | `ec064d6c4fc70ec990911089d966043cb819fba0e26e6f6afdd0a05e5301b91b` |
| [sc-55_v120_mod.bdf](./patches/sc-55_v120_mod.bdf)       | SC-55 Ver.1.20     | `22ce6ca59e6332143b335525e81fab501ea6fccce4b7e2f3bfc2cc8bf6612ff6` |
| [sc-55_v121_mod.bdf](./patches/sc-55_v121_mod.bdf)       | SC-55 Ver.1.21     | `effc6132d68f7e300aaef915ccdd08aba93606c22d23e580daf9ea6617913af1` |
| [sc-55_v200_mod.bdf](./patches/sc-55_v200_mod.bdf)       | SC-55 Ver.2.00     | `f5dac35d450ab986570a209dff3816eec75cee669e161f54b51224b467dd0bcc` |
| [sc-33_v210_mod.bdf](./patches/sc-33_v210_mod.bdf)       | SC-33 Ver.2.10     | `b78f16c0fbee48bc465e05551c675f44ec0f5a5dae908d167459f7922c248de9` |
| [sc-55mk2_v101_mod.bdf](./patches/sc-55mk2_v101_mod.bdf) | SC-55mkII Ver.1.01 | `a4c9fd821059054c7e7681d61f49ce6f42ed2fe407a7ec1ba0dfdc9722582ce0` |
| [sc-55st_v100_mod.bdf](./patches/sc-55st_v100_mod.bdf)   | SC-55ST/SC-55K Ver.1.00 | `03517ac0a3b1ad8b69a1a4ee045e0c21da0170027bd1ba1bd3cf72cd017bbe6a` |


License
-------

MIT


Author
------

[shingo45endo](https://github.com/shingo45endo)
