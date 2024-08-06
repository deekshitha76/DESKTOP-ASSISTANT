$('.tlt').textillate({
    in: {
        effect: 'fadeInDown', // Animation type when text appears
        delayScale: 1.5,      // Scale factor for delays between characters
        delay: 50,            // Delay in milliseconds before each character animation
        sync: false,          // Whether to synchronize all texts or animate them individually
        shuffle: false        // Whether to shuffle the order of the texts
    },
    out: {
        effect: 'fadeOut',    // Animation type when text disappears
        delayScale: 1.5,      // Scale factor for delays between characters during exit
        delay: 50,            // Delay in milliseconds before each character exit animation
        sync: false,          // Whether to synchronize all texts or animate them individually during exit
        shuffle: false        // Whether to shuffle the order of the texts during exit
    },
    loop: true               // Whether to loop the animation continuously
});
