drop table if exists `tcs_cfa_detections`;

create table `tcs_cfa_detections` (
`eventID` int unsigned,
`alertstatus` varchar(12),
`field` varchar(9),
`amp` int unsigned,
`ra` varchar(13),
`decl` varchar(14),
`type` varchar(5),
`visualtype` varchar(11),
`prio` int unsigned,
`date` varchar(10),
`diffsubdir` varchar(21),
`year` int unsigned,
`candID` int unsigned,
`errorflag` bool,
`templ` varchar(7),
`objfile` varchar(44),
`comment` varchar(8),
`specstatus` varchar(11),
`specprio` int unsigned,
`spectel` varchar(46),
`specdate` varchar(36),
`spectype` varchar(9),
`specz` varchar(12),
`speczsource` varchar(19),
`specepoch` varchar(10),
`zphot` varchar(6),
`speccomment` varchar(12),
`originalobjectsfile` varchar(100),
`lastupdate` varchar(21),
`attic` bool,
`public` bool,
`specPI` varchar(20),
`active` bool,
`specgofer` varchar(69),
`eventMJD` float,
`dMJDp` float,
`dMJDm` float,
`g_max` float,
`r_max` float,
`i_max` float,
`z_max` float,
`g_last` float,
`r_last` float,
`i_last` float,
`z_last` float,
`PS1ID` varchar(12),
`queue` varchar(6),
`pubcomment` varchar(11),
`y_max` float,
`y_last` float,
`PS1name` varchar(20),
`pubtype` varchar(8),
`pubconfirm` bool,
`cfa_designation` varchar(15),
`raDeg` double,
`decDeg` double,
`htm20ID` bigint(20) unsigned,
`htm16ID` bigint(20) unsigned,
`cx` double,
`cy` double,
`cz` double,
PRIMARY KEY `idx_eventID` (`eventID`),
KEY `idx_htm20ID` (`htm20ID`),
KEY `idx_htm16ID` (`htm16ID`),
KEY `idx_raDeg_decDeg` (`raDeg`,`decDeg`)
) ENGINE=MyISAM;
