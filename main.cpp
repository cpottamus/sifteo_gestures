/*
 * Sifteo SDK Example.
 */

#include <sifteo.h>
#include "assets.gen.h"
// #include <unistd.h>
using namespace Sifteo;

Metadata M = Metadata()
    .title("USB SDK Example")
    .package("com.sifteo.sdk.usb", "1.0")
    .icon(Icon)
    .cubeRange(2);

/*
 * When you allocate a UsbPipe you can optionally set the size of its transmit and receive queues.
 * We use a minimum-size transmit queue to keep latency low, since we're transmitting continuously.
 */
UsbPipe <1,4> usbPipe;

//Global State Variables for Cube Controls
int touch0;
int tiltx0;
int tilty0;
int tiltz0;
int shake0;
// Byte3 tilt 
// Byte3
// Byte3

// USB packet counters, available for debugging
UsbCounters usbCounters;

VideoBuffer vid[2];
TiltShakeRecognizer motion[2];

void onCubeTouch(void *, unsigned);
void onAccelChange(void *, unsigned);
void onConnect();
void onDisconnect();

void readPacket();
void onReadAvailable();

void writePacket();
void onWriteAvailable();

void updatePacketCounts(int tx, int rx);


void main()
{
    /*
     * Display text in BG0_ROM mode on Cube 0
     */

     //Main Cube
    CubeID cube = 0;
    vid[0].initMode(BG0_ROM);
    vid[0].attach(cube);
    motion[0].attach(cube);
    vid[0].bg0rom.text(vec(0,0), " USB Demo ", vid[0].bg0rom.WHITE_ON_TEAL);

    //Secondary Cube
    CubeID cube2 = 1;
    vid[1].initMode(BG0_ROM);
    vid[1].attach(cube2);
    motion[1].attach(cube2);
    // vid[1].bg0rom.text(vec(0,0), " CUBE 2 TEST", vid[1].bg0rom.WHITE_ON_TEAL);


    // Zero out our counters
    usbCounters.reset();

    /*
     * When we transmit packets in this example, we'll fill them with our
     * cube's accelerometer state. When we receive packets, they'll
     * be hex-dumped to the screen. We also keep counters that show how many
     * packets have been processed.
     *
     * If possible, applications are encouraged to use event handlers so that
     * they only try to read packets when packets are available, and they only
     * write packets when buffer space is available. In this example, we always
     * want to read packets when they arrive, so we keep an onRead() handler
     * registered at all times. We also want to write as long as there's buffer
     * space, but only when a peer is connected. So we'll register and unregister
     * our onWrite() handler in onConnect() and onDisconnect(), respectively.
     *
     * Note that attach() will empty our transmit and receive queues. If we want
     * to enqueue write packets in onConnect(), we need to be sure the pipe is
     * attached before we set up onConnect/onDisconnect.
     */

     //Initialize starting states of globals
     tiltx0 = 0;
     tilty0 = 0;
     tiltz0 = 0;
     touch0 = 0;
     shake0 = 0;
     tiltx1 = 0;
     tilty1 = 0;
     tiltz1 = 0;
     touch1 = 0;
     shake1 = 0;

    Events::usbReadAvailable.set(onReadAvailable);
    usbPipe.attach();
    updatePacketCounts(0, 0);

    /*
     * Watch for incoming connections, and display some text on the screen to
     * indicate connection state.
     */

    Events::usbConnect.set(onConnect);
    Events::usbDisconnect.set(onDisconnect);
    Events::cubeTouch.set(onCubeTouch);
    Events::cubeAccelChange.set(onAccelChange);

    if (Usb::isConnected()) {
        onConnect();
    } else {
        onDisconnect();
    }

    while (1) {

        for (unsigned n = 0; n < 60; n++) {
            readPacket();
            writePacket();
            System::paint();
        }

        /*
         * For debugging, periodically log the USB packet counters.
         */

        usbCounters.capture();
        LOG("USB-Counters: rxPackets=%d txPackets=%d rxBytes=%d txBytes=%d rxUserDropped=%d\n",
            usbCounters.receivedPackets(), usbCounters.sentPackets(),
            usbCounters.receivedBytes(), usbCounters.sentBytes(),
            usbCounters.userPacketsDropped());
    }
}

//Event driven state changes

void onCubeTouch(void* ctxt, unsigned id){
    CubeID cube(id);
    // LOG("TOUCHING? :: %i\n", cube.isTouching());

    if(int(id) == 0){
        if( cube.isTouching()){
            touch0 = 1;
        } else {
            touch0 = 0;
        }
    }

    if(int(id) == 1){
        if( cube.isTouching()){
            touch1 = 1;
        } else {
            touch1 = 0;
        }
    }
    

}

void onAccelChange(void* ctxt, unsigned id){
    CubeID cube(id);
    

    unsigned changeFlags = motion[0].update();
    if(changeFlags) {
        auto tilt = motion[0].tilt;

        tiltx0 = tilt.x;
        tilty0 = tilt.y;
        tiltz0 = tilt.z;

        shake0 = motion[0].shake;
    }

    unsigned changeFlags1 = motion[1].update();
    if(changeFlags) {
        auto tilt1 = motion[1].tilt;

        tiltx1 = tilt1.x;
        tilty1 = tilt1.y;
        tiltz1 = tilt1.z;

        shake1 = motion[1].shake;
    }

}





//USB CONNECTION

void onConnect()
{
    LOG("onConnect() called\n");
    ASSERT(Usb::isConnected());

    vid[0].bg0rom.text(vec(0,2), "   Connected!   ");
    vid[0].bg0rom.text(vec(0,3), "                ");
    vid[0].bg0rom.text(vec(0,8), " Last received: ");

    // Start trying to write immediately
    Events::usbWriteAvailable.set(onWriteAvailable);
    onWriteAvailable();
}

void onDisconnect()
{
    LOG("onDisconnect() called\n");
    ASSERT(!Usb::isConnected());

    vid[0].bg0rom.text(vec(0,2), " Waiting for a  ");
    vid[0].bg0rom.text(vec(0,3), " connection...  ");

    // Stop trying to write
    Events::usbWriteAvailable.unset();
}

void updatePacketCounts(int tx, int rx)
{
    // Update and draw packet counters

    static int txCount = 0;
    static int rxCount = 0;

    txCount += tx;
    rxCount += rx;

    String<17> str;
    str << "RX: " << rxCount;
    vid[0].bg0rom.text(vec(1,6), str);

    str.clear();
    str << "TX: " << txCount;
    vid[0].bg0rom.text(vec(1,5), str);
}

void packetHexDumpLine(const UsbPacket &packet, String<17> &str, unsigned index)
{
    str.clear();

    // Write up to 8 characters
    for (unsigned i = 0; i < 8; ++i, ++index) {
        if (index < packet.size()) {
            str << Hex(packet.bytes()[index], 2);
        } else {
            str << "  ";
        }
    }
}

void onReadAvailable()
{
    LOG("onReadAvailable() called\n");
}

void readPacket()
{
    /*
     * This is one way to read packets from the BluetoothPipe; using read(),
     * and copying them into our own buffer. A faster but slightly more complex
     * method would use peek() to access the next packet, and pop() to remove it.
     *
     * We only attempt to read n packets to avoid the edge case in which packets
     * are arriving often enough to keep us in this loop indefinitely. Not likely
     * a concern for real applications, but keeps things flowing smoothly for
     * this example.
     */

    UsbPacket packet;
    unsigned n = usbPipe.receiveQueue.capacity();

    while (n && usbPipe.read(packet)) {

        n--;

        /*
         * We received a packet over USB!
         * Dump out its contents in hexadecimal, to the log and the display.
         */

        LOG("Received: %d bytes, type=%02x, data=%19h\n",
            packet.size(), packet.type(), packet.bytes());

        String<17> str;

        str << "len=" << Hex(packet.size(), 2) << " type=" << Hex(packet.type(), 2);
        

        //IF TYPE == x, display icon x
        if(packet.type() == 1){
            vid[1].initMode(BG0_SPR_BG1);
            vid[1].bg0.image(vec(0,0), Backgrounds, currentApp[0]);
        }



        vid[0].bg0rom.text(vec(1,10), str);

        packetHexDumpLine(packet, str, 0);
        vid[0].bg0rom.text(vec(0,12), str);

        packetHexDumpLine(packet, str, 8);
        vid[0].bg0rom.text(vec(0,13), str);

        packetHexDumpLine(packet, str, 16);
        vid[0].bg0rom.text(vec(0,14), str);

        // Update our counters
        updatePacketCounts(0, 1);
    }
}

void onWriteAvailable()
{
    // LOG("onWriteAvailable() called\n");

    /*
     * We could potentially write here, though in high throughput scenarios,
     * it's possible for the system to enqueue the writeAvailable event while we're
     * still in this handler, meaning we wouldn't yield back to the main
     * execution context.
     */
}

void writePacket()
{
   /*
    * This is one way to write packets to the UsbPipe; using reserve()
    * and commit(). If you already have a buffer that you want to copy to the
    * UsbPipe, you can use write().
    */

    if (Usb::isConnected() && usbPipe.writeAvailable()) {

        /*
         * Access some buffer space for writing the next packet. This
         * is the zero-copy API for writing packets. Both reading and writing
         * have a traditional (one copy) API and a zero-copy API.
         */

        UsbPacket &packet = usbPipe.sendQueue.reserve();

        /*
         * Fill most of the packet with dummy data
         */

        // 28-bit type code, for our own application's use
        packet.setType(0x5A);

        packet.resize(packet.capacity());

        for (unsigned i = 0; i < packet.capacity(); ++i) {
            packet.bytes()[i] = 0;
        }

        /* 
         * Fill the first 3 bytes with accelerometer data from Cube 0
         */

        ///// Cube 0 //////

        Byte3 accel = vid[0].physicalAccel();

        //accel
        packet.bytes()[0] = accel.x;
        packet.bytes()[1] = accel.y;
        packet.bytes()[2] = accel.z;
        //tilt
        packet.bytes()[3] = tiltx0;
        packet.bytes()[4] = tilty0;
        packet.bytes()[5] = tiltz0;
        packet.bytes()[6] = touch0;
        packet.bytes()[7] = shake0;

        ///// Cube 1 //////

        Byte3 accel1 = vid[1].physicalAccel();

        //accel
        packet.bytes()[8] = accel1.x;
        packet.bytes()[9] = accel1.y;
        packet.bytes()[10] = accel1.z;
        //tilt
        packet.bytes()[11] = tiltx1;
        packet.bytes()[12] = tilty1;
        packet.bytes()[13] = tiltz1;
        packet.bytes()[14] = touch1;
        packet.bytes()[15] = shake1;

        /*
         * Log the packet for debugging, and commit it to the FIFO.
         * The system will asynchronously send it to our peer.
         */

        // LOG("Sending: %d bytes, type=%02x, data=%19h\n",
        //     packet.size(), packet.type(), packet.bytes());

        usbPipe.sendQueue.commit();
        updatePacketCounts(1, 0);
    }
}
