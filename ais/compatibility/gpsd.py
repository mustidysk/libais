class Mangler(object):
    def __call__(self, msg):
        res = {}
        self.mangle(res, msg)
        for key in msg:
            method = 'mangle__' + key
            if hasattr(self, method):
                getattr(self, method)(res, msg)
            else:
                res[key] = msg[key]
        return res

    def mangle(self, res, msg):
        res['class'] = "AIS"
        res['device'] = "stdin"
        res['scaled'] = True
        if msg['id'] in (1, 2, 3):
            res['status'] = self.nav_statuses[15]
            res['heading'] = 511

    def mangle__id(self, res, msg):
        res['type'] = msg['id']

    #### Types 1, 2 and 3: Position Report Class A ####

    def mangle__cog(self, res, msg):
        res['course'] = msg['cog']

    def mangle__nav_status(self, res, msg):
        res['status'] = self.nav_statuses[msg['nav_status']]

    def mangle__position_accuracy(self, res, msg):
        res['accuracy'] = msg['position_accuracy'] == 1

    def mangle__repeat_indicator(self, res, msg):
        res['repeat'] = msg['repeat_indicator']

    # rot, rot_over_range, slot_timeout

    def mangle__sog(self, res, msg):
        res['speed'] = msg['sog']

    # spare, special_manoeuvre, sync_state, timestamp

    def mangle__true_heading(self, res, msg):
        res['heading'] = msg['true_heading']

    # utc_hour, utc_min, utc_spare

    def mangle__x(self, res, msg):
        res['lon'] = msg['x']

    def mangle__y(self, res, msg):
        res['lat'] = msg['y']

    #### Type 4: Base Station Report ####

    def mangle__year(self, res, msg):
        res['eta'] = "%04d-%02d-%02dT%02d:%02d:%02dZ" % (msg['year'], msg['month'], msg['day'], msg['hour'], msg['minute'], msg['second'])

    def mangle__month(self, res, msg): pass
    def mangle__day(self, res, msg): pass
    def mangle__hour(self, res, msg): pass
    def mangle__minute(self, res, msg): pass
    def mangle__second(self, res, msg): pass

    def mangle__fix_type(self, res, msg):
        res['epfd'] = self.fix_types.get(msg['fix_type'], self.fix_types[0])

    #### Type 5: Static and Voyage Related Data  #####

    def mangle__dim_a(self, res, msg):
        res['to_bow'] = msg['dim_a']

    def mangle__dim_b(self, res, msg):
        res['to_stern'] = msg['dim_b']

    def mangle__dim_c(self, res, msg):
        res['to_port'] = msg['dim_c']

    def mangle__dim_d(self, res, msg):
        res['to_starboard'] = msg['dim_d']

    def mangle__eta_day(self, res, msg):
        res['eta'] = "%02d-%02dT%02d:%02dZ" % (msg['eta_month'], msg['eta_day'], msg['eta_hour'], msg['eta_minute'])

    def mangle__eta_hour(self, res, msg): pass
    def mangle__eta_minute(self, res, msg): pass
    def mangle__eta_month(self, res, msg): pass

    #### Type 6: Binary Addressed Message ####

    def mangle__mmsi_dest(self, res, msg):
        res['dest_mmsi'] = msg['mmsi_dest']

    def mangle__seq(self, res, msg):
        res['seqno'] = msg['seq']

    # Note: retransmit has different values for the same message from gpsd... bug?

    #### Type 8: Binary Broadcast Message ####

    def mangle__fi(self, res, msg):
        res['fid'] = msg['fi']

    # Note: Data is missing from libais message

    #### Type 9: Standard SAR Aircraft Position Report ####

    def mangle__timestamp(self, res, msg):
        res['second'] = msg['timestamp']

    #### Type 17: DGNSS Broadcast Binary Message ####

    # Note: Data is missing from libais message

    #### Type 18: Standard Class B CS Position Report #####

    def mangle__band_flag(self, res, msg):
        res['band'] = msg['band_flag'] == 1

    def mangle__commstate_flag(self, res, msg):
        res['cs'] = msg['commstate_flag'] == 1

    def mangle__display_flag(self, res, msg):
        res['display'] = msg['display_flag'] == 1

    def mangle__dsc_flag(self, res, msg):
        res['dsc'] = msg['dsc_flag'] == 1

    def mangle__m22_flag(self, res, msg):
        res['msg22'] = msg['m22_flag'] == 1

    def mangle__mode_flag(self, res, msg):
        res['mode'] = msg['mode_flag'] == 1

    def mangle__unit_flag(self, res, msg):
        res['unit'] = msg['unit_flag'] == 1

    #### Type 19: Extended Class B CS Position Report ####

    def mangle__assigned_mode(self, res, msg):
        res['assigned'] = msg['assigned_mode'] == 1

    #### Type 20 Data Link Management Message ####

    def mangle__reservations(self, res, msg):
        for idx, reservation in enumerate(msg['reservations']):
            i = str(idx + 1)
            res['increment' + i] = reservation['incr']
            res['number' + i] = reservation['num_slots']
            res['offset' + i] = reservation['offset']
            res['timeout' + i] = reservation['timeout']

    #### Type 21: Aid-to-Navigation Report ####

    def mangle__aton_type(self, res, msg):
        res['aid_type'] = self.aton_types[msg['aton_type']]

    def mangle__name(self, res, msg):
        res['name'] = msg['name'].rstrip("@")

    def mangle__off_pos(self, res, msg):
        res['off_position'] = msg['off_pos']

    def mangle__virtual_aton(self, res, msg):
        res['virtual_aid'] = msg['virtual_aton']

    
    #### Type 22: Channel Management ####

    def mangle__chan_a(self, res, msg):
        res['channel_a'] = msg['chan_a']

    def mangle__chan_b(self, res, msg):
        res['channel_b'] = msg['chan_b']

    def mangle__chan_a_bandwidth(self, res, msg):
        res['band_a'] = msg['chan_a_bandwidth']

    def mangle__chan_b_bandwidth(self, res, msg):
        res['band_b'] = msg['chan_b_bandwidth']

    def mangle__power_low(self, res, msg):
        res['power'] = msg['power_low']

    def mangle__txrx_mode(self, res, msg):
        res['txrx'] = msg['txrx_mode']

    def mangle__x1(self, res, msg):
        res['ne_lon'] = msg['x1']

    def mangle__x2(self, res, msg):
        res['sw_lon'] = msg['x2']

    def mangle__y1(self, res, msg):
        res['sw_lat'] = msg['y2']

    def mangle__y1(self, res, msg):
        res['ne_lat'] = msg['y1']

    def mangle__zone_size(self, res, msg):
        res['zonesize'] = msg['zone_size']

    #### Mappings ####

    aton_types = {
        0: "Default, Type of Aid to Navigation not specified",
        1: "Reference point",
        2: "RACON (radar transponder marking a navigation hazard)",
        3: "Fixed structure off shore, such as oil platforms, wind farms, rigs.",
        4: "Spare, Reserved for future use.",
        5: "Light, without sectors",
        6: "Light, with sectors",
        7: "Leading Light Front",
        8: "Leading Light Rear",
        9: "Beacon, Cardinal N",
        10: "Beacon, Cardinal E",
        11: "Beacon, Cardinal S",
        12: "Beacon, Cardinal W",
        13: "Beacon, Port hand",
        14: "Beacon, Starboard hand",
        15: "Beacon, Preferred Channel port hand",
        16: "Beacon, Preferred Channel starboard hand",
        17: "Beacon, Isolated danger",
        18: "Beacon, Safe water",
        19: "Beacon, Special mark",
        20: "Cardinal Mark N",
        21: "Cardinal Mark E",
        22: "Cardinal Mark S",
        23: "Cardinal Mark W",
        24: "Port hand Mark",
        25: "Starboard hand Mark",
        26: "Preferred Channel Port hand",
        27: "Preferred Channel Starboard hand",
        28: "Isolated danger",
        29: "Safe Water",
        30: "Special Mark",
        31: "Light Vessel / LANBY / Rigs"
    }

    fix_types = {
        0: "Undefined",
        1: "GPS",
        2: "GLONASS",
        3: "Combined GPS/GLONASS",
        4: "Loran-C",
        5: "Chayka",
        6: "Integrated navigation system",
        7: "Surveyed",
        8: "Galileo"
    }

    nav_statuses = {
        0: "under way using engine",
        1: "at anchor",
        2: "not under command",
        3: "restricted maneuverability",
        4: "constrained by her draught",
        5: "moored",
        6: "aground",
        7: "engaged in fishing",
        8: "under way sailing",
        9: "reserved for future amendment of navigational status for ships carrying DG, HS, or MP, or IMO hazard or pollutant category C, high speed craft (HSC)",
        10: "reserved for future amendment of navigational status for ships carrying dangerous goods (DG), harmful substances (HS) or marine pollutants (MP), or IMO hazard or pollutant category A, wing in ground (WIG)",
        11: "power-driven vessel towing astern (regional use)",
        12: "power-driven vessel pushing ahead or towing alongside (regional use)",
        13: "reserved for future use",
        14: "AIS-SART (active), MOB-AIS, EPIRB-AIS",
        15: "default (also used by AIS-SART, MOB-AIS and EPIRB-AIS under test)"
        }


mangle = Mangler()