var defaultCategories = [
    { title: "Arduino", slug: "arduino" },
    { title: "Raspberry Pi", slug: "raspberry-pi" },
    { title: "Beaglebone", slug: "beaglebone" },
    { title: "Xbee", slug: "xbee" },
    { title: "Neopixels", slug: "neopixels" },
    { title: "Prototyping", slug: "prototyping" },
    { title: "Components", slug: "components" },
    { title: "LEDs", slug: "leds" },
    { title: "Power", slug: "power" },
    { title: "Sensors", slug: "sensors" },
    { title: "Cables", slug: "cables" },
    { title: "Tools", slug: "tools" },
    { title: "Displays", slug: "displays" }
];


if ( Categories.find().count() === 0 ) {
    _.each( defaultCategories, function ( doc ) {
        Categories.insert( doc );
    } );
}
