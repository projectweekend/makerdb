var defaultTags = [
    { slug: "arduino" },
    { slug: "raspberry-pi" },
    { slug: "prototyping" },
    { slug: "resistor" },
    { slug: "capacitor" },
    { slug: "led" },
    { slug: "power" },
    { slug: "sensor" },
    { slug: "cable" },
    { slug: "tool" }
];


if ( Tags.find().count() === 0 ) {
    _.each( defaultTags, function ( doc ) {
        Tags.insert( doc );
    } );
}
