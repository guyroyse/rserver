"""
Reticulum Link management layer.
Handles raw Link connections and data transfer.
"""

import RNS

# Global reference to data handler
_data_handler = None


def start_link_server(destination, data_handler):
    """Start accepting Link connections on destination with data handler."""
    global _data_handler
    _data_handler = data_handler
    
    destination.set_link_established_callback(on_link_established)
    print(f"✓ Link server listening")


def on_link_established(link):
    """Called when a Link connection is established."""
    print(f"✓ Link established")
    
    link.set_packet_callback(on_packet_received)
    link.set_link_closed_callback(on_link_closed)


def on_packet_received(data, packet):
    """Handle incoming data from a Link."""
    try:
        # Pass raw data to handler
        response_data = _data_handler(data)
        
        # Send response back if provided
        if response_data:
            response_packet = RNS.Packet(packet.link, response_data)
            response_packet.send()
            
    except Exception as e:
        print(f"✗ Link error: {e}")


def on_link_closed(link):
    """Called when a Link connection is closed."""
    print("✓ Link closed")
