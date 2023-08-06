Features not yet supported, but planned:
- Support for multiple MacroServers sharing Pools
- Support for excluding Pools from the config (e.g. pools that are configured in other ways)
- MacroServer environment configuration

Issues:
- If a Sardana/xyz instance is split into separate Pool/MS instances, the old Sardana/xyz server is still around, even if empty. Probably this goes both ways. Maybe dsconfig should clean empty servers up.
- I think we leave aliases around when removing devices. I had expected the tango DB to not allow dangling aliases, but apparently this is not the case. Probably also something that dsconfig should handle.
