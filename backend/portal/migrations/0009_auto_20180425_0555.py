# Generated by Django 2.0.2 on 2018-04-25 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0008_settings_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('en', 'English'), ('de', 'German')], max_length=10, null=True)),
                ('timezone', models.IntegerField(blank=True, choices=[(0, 'Africa/Abidjan'), (1, 'Africa/Accra'), (2, 'Africa/Addis_Ababa'), (3, 'Africa/Algiers'), (4, 'Africa/Asmara'), (5, 'Africa/Asmera'), (6, 'Africa/Bamako'), (7, 'Africa/Bangui'), (8, 'Africa/Banjul'), (9, 'Africa/Bissau'), (10, 'Africa/Blantyre'), (11, 'Africa/Brazzaville'), (12, 'Africa/Bujumbura'), (13, 'Africa/Cairo'), (14, 'Africa/Casablanca'), (15, 'Africa/Ceuta'), (16, 'Africa/Conakry'), (17, 'Africa/Dakar'), (18, 'Africa/Dar_es_Salaam'), (19, 'Africa/Djibouti'), (20, 'Africa/Douala'), (21, 'Africa/El_Aaiun'), (22, 'Africa/Freetown'), (23, 'Africa/Gaborone'), (24, 'Africa/Harare'), (25, 'Africa/Johannesburg'), (26, 'Africa/Juba'), (27, 'Africa/Kampala'), (28, 'Africa/Khartoum'), (29, 'Africa/Kigali'), (30, 'Africa/Kinshasa'), (31, 'Africa/Lagos'), (32, 'Africa/Libreville'), (33, 'Africa/Lome'), (34, 'Africa/Luanda'), (35, 'Africa/Lubumbashi'), (36, 'Africa/Lusaka'), (37, 'Africa/Malabo'), (38, 'Africa/Maputo'), (39, 'Africa/Maseru'), (40, 'Africa/Mbabane'), (41, 'Africa/Mogadishu'), (42, 'Africa/Monrovia'), (43, 'Africa/Nairobi'), (44, 'Africa/Ndjamena'), (45, 'Africa/Niamey'), (46, 'Africa/Nouakchott'), (47, 'Africa/Ouagadougou'), (48, 'Africa/Porto-Novo'), (49, 'Africa/Sao_Tome'), (50, 'Africa/Timbuktu'), (51, 'Africa/Tripoli'), (52, 'Africa/Tunis'), (53, 'Africa/Windhoek'), (54, 'America/Adak'), (55, 'America/Anchorage'), (56, 'America/Anguilla'), (57, 'America/Antigua'), (58, 'America/Araguaina'), (59, 'America/Argentina/Buenos_Aires'), (60, 'America/Argentina/Catamarca'), (61, 'America/Argentina/ComodRivadavia'), (62, 'America/Argentina/Cordoba'), (63, 'America/Argentina/Jujuy'), (64, 'America/Argentina/La_Rioja'), (65, 'America/Argentina/Mendoza'), (66, 'America/Argentina/Rio_Gallegos'), (67, 'America/Argentina/Salta'), (68, 'America/Argentina/San_Juan'), (69, 'America/Argentina/San_Luis'), (70, 'America/Argentina/Tucuman'), (71, 'America/Argentina/Ushuaia'), (72, 'America/Aruba'), (73, 'America/Asuncion'), (74, 'America/Atikokan'), (75, 'America/Atka'), (76, 'America/Bahia'), (77, 'America/Bahia_Banderas'), (78, 'America/Barbados'), (79, 'America/Belem'), (80, 'America/Belize'), (81, 'America/Blanc-Sablon'), (82, 'America/Boa_Vista'), (83, 'America/Bogota'), (84, 'America/Boise'), (85, 'America/Buenos_Aires'), (86, 'America/Cambridge_Bay'), (87, 'America/Campo_Grande'), (88, 'America/Cancun'), (89, 'America/Caracas'), (90, 'America/Catamarca'), (91, 'America/Cayenne'), (92, 'America/Cayman'), (93, 'America/Chicago'), (94, 'America/Chihuahua'), (95, 'America/Coral_Harbour'), (96, 'America/Cordoba'), (97, 'America/Costa_Rica'), (98, 'America/Creston'), (99, 'America/Cuiaba'), (100, 'America/Curacao'), (101, 'America/Danmarkshavn'), (102, 'America/Dawson'), (103, 'America/Dawson_Creek'), (104, 'America/Denver'), (105, 'America/Detroit'), (106, 'America/Dominica'), (107, 'America/Edmonton'), (108, 'America/Eirunepe'), (109, 'America/El_Salvador'), (110, 'America/Ensenada'), (111, 'America/Fort_Nelson'), (112, 'America/Fort_Wayne'), (113, 'America/Fortaleza'), (114, 'America/Glace_Bay'), (115, 'America/Godthab'), (116, 'America/Goose_Bay'), (117, 'America/Grand_Turk'), (118, 'America/Grenada'), (119, 'America/Guadeloupe'), (120, 'America/Guatemala'), (121, 'America/Guayaquil'), (122, 'America/Guyana'), (123, 'America/Halifax'), (124, 'America/Havana'), (125, 'America/Hermosillo'), (126, 'America/Indiana/Indianapolis'), (127, 'America/Indiana/Knox'), (128, 'America/Indiana/Marengo'), (129, 'America/Indiana/Petersburg'), (130, 'America/Indiana/Tell_City'), (131, 'America/Indiana/Vevay'), (132, 'America/Indiana/Vincennes'), (133, 'America/Indiana/Winamac'), (134, 'America/Indianapolis'), (135, 'America/Inuvik'), (136, 'America/Iqaluit'), (137, 'America/Jamaica'), (138, 'America/Jujuy'), (139, 'America/Juneau'), (140, 'America/Kentucky/Louisville'), (141, 'America/Kentucky/Monticello'), (142, 'America/Knox_IN'), (143, 'America/Kralendijk'), (144, 'America/La_Paz'), (145, 'America/Lima'), (146, 'America/Los_Angeles'), (147, 'America/Louisville'), (148, 'America/Lower_Princes'), (149, 'America/Maceio'), (150, 'America/Managua'), (151, 'America/Manaus'), (152, 'America/Marigot'), (153, 'America/Martinique'), (154, 'America/Matamoros'), (155, 'America/Mazatlan'), (156, 'America/Mendoza'), (157, 'America/Menominee'), (158, 'America/Merida'), (159, 'America/Metlakatla'), (160, 'America/Mexico_City'), (161, 'America/Miquelon'), (162, 'America/Moncton'), (163, 'America/Monterrey'), (164, 'America/Montevideo'), (165, 'America/Montreal'), (166, 'America/Montserrat'), (167, 'America/Nassau'), (168, 'America/New_York'), (169, 'America/Nipigon'), (170, 'America/Nome'), (171, 'America/Noronha'), (172, 'America/North_Dakota/Beulah'), (173, 'America/North_Dakota/Center'), (174, 'America/North_Dakota/New_Salem'), (175, 'America/Ojinaga'), (176, 'America/Panama'), (177, 'America/Pangnirtung'), (178, 'America/Paramaribo'), (179, 'America/Phoenix'), (180, 'America/Port-au-Prince'), (181, 'America/Port_of_Spain'), (182, 'America/Porto_Acre'), (183, 'America/Porto_Velho'), (184, 'America/Puerto_Rico'), (185, 'America/Punta_Arenas'), (186, 'America/Rainy_River'), (187, 'America/Rankin_Inlet'), (188, 'America/Recife'), (189, 'America/Regina'), (190, 'America/Resolute'), (191, 'America/Rio_Branco'), (192, 'America/Rosario'), (193, 'America/Santa_Isabel'), (194, 'America/Santarem'), (195, 'America/Santiago'), (196, 'America/Santo_Domingo'), (197, 'America/Sao_Paulo'), (198, 'America/Scoresbysund'), (199, 'America/Shiprock'), (200, 'America/Sitka'), (201, 'America/St_Barthelemy'), (202, 'America/St_Johns'), (203, 'America/St_Kitts'), (204, 'America/St_Lucia'), (205, 'America/St_Thomas'), (206, 'America/St_Vincent'), (207, 'America/Swift_Current'), (208, 'America/Tegucigalpa'), (209, 'America/Thule'), (210, 'America/Thunder_Bay'), (211, 'America/Tijuana'), (212, 'America/Toronto'), (213, 'America/Tortola'), (214, 'America/Vancouver'), (215, 'America/Virgin'), (216, 'America/Whitehorse'), (217, 'America/Winnipeg'), (218, 'America/Yakutat'), (219, 'America/Yellowknife'), (220, 'Antarctica/Casey'), (221, 'Antarctica/Davis'), (222, 'Antarctica/DumontDUrville'), (223, 'Antarctica/Macquarie'), (224, 'Antarctica/Mawson'), (225, 'Antarctica/McMurdo'), (226, 'Antarctica/Palmer'), (227, 'Antarctica/Rothera'), (228, 'Antarctica/South_Pole'), (229, 'Antarctica/Syowa'), (230, 'Antarctica/Troll'), (231, 'Antarctica/Vostok'), (232, 'Arctic/Longyearbyen'), (233, 'Asia/Aden'), (234, 'Asia/Almaty'), (235, 'Asia/Amman'), (236, 'Asia/Anadyr'), (237, 'Asia/Aqtau'), (238, 'Asia/Aqtobe'), (239, 'Asia/Ashgabat'), (240, 'Asia/Ashkhabad'), (241, 'Asia/Atyrau'), (242, 'Asia/Baghdad'), (243, 'Asia/Bahrain'), (244, 'Asia/Baku'), (245, 'Asia/Bangkok'), (246, 'Asia/Barnaul'), (247, 'Asia/Beirut'), (248, 'Asia/Bishkek'), (249, 'Asia/Brunei'), (250, 'Asia/Calcutta'), (251, 'Asia/Chita'), (252, 'Asia/Choibalsan'), (253, 'Asia/Chongqing'), (254, 'Asia/Chungking'), (255, 'Asia/Colombo'), (256, 'Asia/Dacca'), (257, 'Asia/Damascus'), (258, 'Asia/Dhaka'), (259, 'Asia/Dili'), (260, 'Asia/Dubai'), (261, 'Asia/Dushanbe'), (262, 'Asia/Famagusta'), (263, 'Asia/Gaza'), (264, 'Asia/Harbin'), (265, 'Asia/Hebron'), (266, 'Asia/Ho_Chi_Minh'), (267, 'Asia/Hong_Kong'), (268, 'Asia/Hovd'), (269, 'Asia/Irkutsk'), (270, 'Asia/Istanbul'), (271, 'Asia/Jakarta'), (272, 'Asia/Jayapura'), (273, 'Asia/Jerusalem'), (274, 'Asia/Kabul'), (275, 'Asia/Kamchatka'), (276, 'Asia/Karachi'), (277, 'Asia/Kashgar'), (278, 'Asia/Kathmandu'), (279, 'Asia/Katmandu'), (280, 'Asia/Khandyga'), (281, 'Asia/Kolkata'), (282, 'Asia/Krasnoyarsk'), (283, 'Asia/Kuala_Lumpur'), (284, 'Asia/Kuching'), (285, 'Asia/Kuwait'), (286, 'Asia/Macao'), (287, 'Asia/Macau'), (288, 'Asia/Magadan'), (289, 'Asia/Makassar'), (290, 'Asia/Manila'), (291, 'Asia/Muscat'), (292, 'Asia/Nicosia'), (293, 'Asia/Novokuznetsk'), (294, 'Asia/Novosibirsk'), (295, 'Asia/Omsk'), (296, 'Asia/Oral'), (297, 'Asia/Phnom_Penh'), (298, 'Asia/Pontianak'), (299, 'Asia/Pyongyang'), (300, 'Asia/Qatar'), (301, 'Asia/Qyzylorda'), (302, 'Asia/Rangoon'), (303, 'Asia/Riyadh'), (304, 'Asia/Saigon'), (305, 'Asia/Sakhalin'), (306, 'Asia/Samarkand'), (307, 'Asia/Seoul'), (308, 'Asia/Shanghai'), (309, 'Asia/Singapore'), (310, 'Asia/Srednekolymsk'), (311, 'Asia/Taipei'), (312, 'Asia/Tashkent'), (313, 'Asia/Tbilisi'), (314, 'Asia/Tehran'), (315, 'Asia/Tel_Aviv'), (316, 'Asia/Thimbu'), (317, 'Asia/Thimphu'), (318, 'Asia/Tokyo'), (319, 'Asia/Tomsk'), (320, 'Asia/Ujung_Pandang'), (321, 'Asia/Ulaanbaatar'), (322, 'Asia/Ulan_Bator'), (323, 'Asia/Urumqi'), (324, 'Asia/Ust-Nera'), (325, 'Asia/Vientiane'), (326, 'Asia/Vladivostok'), (327, 'Asia/Yakutsk'), (328, 'Asia/Yangon'), (329, 'Asia/Yekaterinburg'), (330, 'Asia/Yerevan'), (331, 'Atlantic/Azores'), (332, 'Atlantic/Bermuda'), (333, 'Atlantic/Canary'), (334, 'Atlantic/Cape_Verde'), (335, 'Atlantic/Faeroe'), (336, 'Atlantic/Faroe'), (337, 'Atlantic/Jan_Mayen'), (338, 'Atlantic/Madeira'), (339, 'Atlantic/Reykjavik'), (340, 'Atlantic/South_Georgia'), (341, 'Atlantic/St_Helena'), (342, 'Atlantic/Stanley'), (343, 'Australia/ACT'), (344, 'Australia/Adelaide'), (345, 'Australia/Brisbane'), (346, 'Australia/Broken_Hill'), (347, 'Australia/Canberra'), (348, 'Australia/Currie'), (349, 'Australia/Darwin'), (350, 'Australia/Eucla'), (351, 'Australia/Hobart'), (352, 'Australia/LHI'), (353, 'Australia/Lindeman'), (354, 'Australia/Lord_Howe'), (355, 'Australia/Melbourne'), (356, 'Australia/NSW'), (357, 'Australia/North'), (358, 'Australia/Perth'), (359, 'Australia/Queensland'), (360, 'Australia/South'), (361, 'Australia/Sydney'), (362, 'Australia/Tasmania'), (363, 'Australia/Victoria'), (364, 'Australia/West'), (365, 'Australia/Yancowinna'), (366, 'Brazil/Acre'), (367, 'Brazil/DeNoronha'), (368, 'Brazil/East'), (369, 'Brazil/West'), (370, 'CET'), (371, 'CST6CDT'), (372, 'Canada/Atlantic'), (373, 'Canada/Central'), (374, 'Canada/Eastern'), (375, 'Canada/Mountain'), (376, 'Canada/Newfoundland'), (377, 'Canada/Pacific'), (378, 'Canada/Saskatchewan'), (379, 'Canada/Yukon'), (380, 'Chile/Continental'), (381, 'Chile/EasterIsland'), (382, 'Cuba'), (383, 'EET'), (384, 'EST'), (385, 'EST5EDT'), (386, 'Egypt'), (387, 'Eire'), (388, 'Etc/GMT'), (389, 'Etc/GMT+0'), (390, 'Etc/GMT+1'), (391, 'Etc/GMT+10'), (392, 'Etc/GMT+11'), (393, 'Etc/GMT+12'), (394, 'Etc/GMT+2'), (395, 'Etc/GMT+3'), (396, 'Etc/GMT+4'), (397, 'Etc/GMT+5'), (398, 'Etc/GMT+6'), (399, 'Etc/GMT+7'), (400, 'Etc/GMT+8'), (401, 'Etc/GMT+9'), (402, 'Etc/GMT-0'), (403, 'Etc/GMT-1'), (404, 'Etc/GMT-10'), (405, 'Etc/GMT-11'), (406, 'Etc/GMT-12'), (407, 'Etc/GMT-13'), (408, 'Etc/GMT-14'), (409, 'Etc/GMT-2'), (410, 'Etc/GMT-3'), (411, 'Etc/GMT-4'), (412, 'Etc/GMT-5'), (413, 'Etc/GMT-6'), (414, 'Etc/GMT-7'), (415, 'Etc/GMT-8'), (416, 'Etc/GMT-9'), (417, 'Etc/GMT0'), (418, 'Etc/Greenwich'), (419, 'Etc/UCT'), (420, 'Etc/UTC'), (421, 'Etc/Universal'), (422, 'Etc/Zulu'), (423, 'Europe/Amsterdam'), (424, 'Europe/Andorra'), (425, 'Europe/Astrakhan'), (426, 'Europe/Athens'), (427, 'Europe/Belfast'), (428, 'Europe/Belgrade'), (429, 'Europe/Berlin'), (430, 'Europe/Bratislava'), (431, 'Europe/Brussels'), (432, 'Europe/Bucharest'), (433, 'Europe/Budapest'), (434, 'Europe/Busingen'), (435, 'Europe/Chisinau'), (436, 'Europe/Copenhagen'), (437, 'Europe/Dublin'), (438, 'Europe/Gibraltar'), (439, 'Europe/Guernsey'), (440, 'Europe/Helsinki'), (441, 'Europe/Isle_of_Man'), (442, 'Europe/Istanbul'), (443, 'Europe/Jersey'), (444, 'Europe/Kaliningrad'), (445, 'Europe/Kiev'), (446, 'Europe/Kirov'), (447, 'Europe/Lisbon'), (448, 'Europe/Ljubljana'), (449, 'Europe/London'), (450, 'Europe/Luxembourg'), (451, 'Europe/Madrid'), (452, 'Europe/Malta'), (453, 'Europe/Mariehamn'), (454, 'Europe/Minsk'), (455, 'Europe/Monaco'), (456, 'Europe/Moscow'), (457, 'Europe/Nicosia'), (458, 'Europe/Oslo'), (459, 'Europe/Paris'), (460, 'Europe/Podgorica'), (461, 'Europe/Prague'), (462, 'Europe/Riga'), (463, 'Europe/Rome'), (464, 'Europe/Samara'), (465, 'Europe/San_Marino'), (466, 'Europe/Sarajevo'), (467, 'Europe/Saratov'), (468, 'Europe/Simferopol'), (469, 'Europe/Skopje'), (470, 'Europe/Sofia'), (471, 'Europe/Stockholm'), (472, 'Europe/Tallinn'), (473, 'Europe/Tirane'), (474, 'Europe/Tiraspol'), (475, 'Europe/Ulyanovsk'), (476, 'Europe/Uzhgorod'), (477, 'Europe/Vaduz'), (478, 'Europe/Vatican'), (479, 'Europe/Vienna'), (480, 'Europe/Vilnius'), (481, 'Europe/Volgograd'), (482, 'Europe/Warsaw'), (483, 'Europe/Zagreb'), (484, 'Europe/Zaporozhye'), (485, 'Europe/Zurich'), (486, 'GB'), (487, 'GB-Eire'), (488, 'GMT'), (489, 'GMT+0'), (490, 'GMT-0'), (491, 'GMT0'), (492, 'Greenwich'), (493, 'HST'), (494, 'Hongkong'), (495, 'Iceland'), (496, 'Indian/Antananarivo'), (497, 'Indian/Chagos'), (498, 'Indian/Christmas'), (499, 'Indian/Cocos'), (500, 'Indian/Comoro'), (501, 'Indian/Kerguelen'), (502, 'Indian/Mahe'), (503, 'Indian/Maldives'), (504, 'Indian/Mauritius'), (505, 'Indian/Mayotte'), (506, 'Indian/Reunion'), (507, 'Iran'), (508, 'Israel'), (509, 'Jamaica'), (510, 'Japan'), (511, 'Kwajalein'), (512, 'Libya'), (513, 'MET'), (514, 'MST'), (515, 'MST7MDT'), (516, 'Mexico/BajaNorte'), (517, 'Mexico/BajaSur'), (518, 'Mexico/General'), (519, 'NZ'), (520, 'NZ-CHAT'), (521, 'Navajo'), (522, 'PRC'), (523, 'PST8PDT'), (524, 'Pacific/Apia'), (525, 'Pacific/Auckland'), (526, 'Pacific/Bougainville'), (527, 'Pacific/Chatham'), (528, 'Pacific/Chuuk'), (529, 'Pacific/Easter'), (530, 'Pacific/Efate'), (531, 'Pacific/Enderbury'), (532, 'Pacific/Fakaofo'), (533, 'Pacific/Fiji'), (534, 'Pacific/Funafuti'), (535, 'Pacific/Galapagos'), (536, 'Pacific/Gambier'), (537, 'Pacific/Guadalcanal'), (538, 'Pacific/Guam'), (539, 'Pacific/Honolulu'), (540, 'Pacific/Johnston'), (541, 'Pacific/Kiritimati'), (542, 'Pacific/Kosrae'), (543, 'Pacific/Kwajalein'), (544, 'Pacific/Majuro'), (545, 'Pacific/Marquesas'), (546, 'Pacific/Midway'), (547, 'Pacific/Nauru'), (548, 'Pacific/Niue'), (549, 'Pacific/Norfolk'), (550, 'Pacific/Noumea'), (551, 'Pacific/Pago_Pago'), (552, 'Pacific/Palau'), (553, 'Pacific/Pitcairn'), (554, 'Pacific/Pohnpei'), (555, 'Pacific/Ponape'), (556, 'Pacific/Port_Moresby'), (557, 'Pacific/Rarotonga'), (558, 'Pacific/Saipan'), (559, 'Pacific/Samoa'), (560, 'Pacific/Tahiti'), (561, 'Pacific/Tarawa'), (562, 'Pacific/Tongatapu'), (563, 'Pacific/Truk'), (564, 'Pacific/Wake'), (565, 'Pacific/Wallis'), (566, 'Pacific/Yap'), (567, 'Poland'), (568, 'Portugal'), (569, 'ROC'), (570, 'ROK'), (571, 'Singapore'), (572, 'Turkey'), (573, 'UCT'), (574, 'US/Alaska'), (575, 'US/Aleutian'), (576, 'US/Arizona'), (577, 'US/Central'), (578, 'US/East-Indiana'), (579, 'US/Eastern'), (580, 'US/Hawaii'), (581, 'US/Indiana-Starke'), (582, 'US/Michigan'), (583, 'US/Mountain'), (584, 'US/Pacific'), (585, 'US/Samoa'), (586, 'UTC'), (587, 'Universal'), (588, 'W-SU'), (589, 'WET'), (590, 'Zulu')], null=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('billing_vat_code', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublisherMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_contact', models.BooleanField(default=False)),
                ('is_primary_contact', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='portal.Publisher')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='settings',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='portal.Publisher'),
        ),
    ]
