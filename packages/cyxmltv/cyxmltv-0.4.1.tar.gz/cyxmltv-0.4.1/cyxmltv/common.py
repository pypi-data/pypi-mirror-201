from collections import namedtuple

TVShow = namedtuple("TVShow", ["start_time",
                               "end_time",
                               "name",
                               "description"])
Channel = namedtuple("Channel", ["name",
                                 "id",
                                 "icon",
                                 "shows"])


ChannelMappings = dict({
    "ch26": "ANT1",
    "ch27": "RIK 1",
    "ch28": "RIK 2",
    "ch29": "Omega",
    "ch30": "Sigma",
    "ch32": "Extra",
    "ch39": "Plus",
    "ch54": "Capital TV",
    "ch82": "4E",
    "ch83": "ERT World",
    "ch84": "Vouli",
    "ch151": "Alpha Cyprus",
    "ch152": "TV Mall",
    "ch178": "Action 24",
    "ch199": "TNT Cyprus",
})
