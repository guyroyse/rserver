#!/usr/bin/env python3
"""
Simple test client for RServer Link layer.
"""

import RNS
import sys
import time


def main():
    print("RServer Test Client")
    print("=" * 30)
    
    if len(sys.argv) != 2:
        print("Usage: python test_client.py <destination_hash>")
        print("Example: python test_client.py a1b2c3d4e5f6...")
        sys.exit(1)
        
    destination_hash = sys.argv[1]
    
    try:
        # Initialize Reticulum
        print("Initializing Reticulum...")
        RNS.Reticulum()
        print("✓ Reticulum initialized")
        
        # Convert destination hash string to bytes
        try:
            dest_hash = bytes.fromhex(destination_hash)
        except ValueError:
            print("✗ Invalid destination hash format")
            sys.exit(1)
            
        # Create identity for client
        identity = RNS.Identity()
        print(f"✓ Client identity: {RNS.prettyhexrep(identity.hash)}")
        
        # Request path to destination
        print(f"Looking for destination: {destination_hash}")
        if not RNS.Transport.has_path(dest_hash):
            print("✓ Requesting path to destination...")
            RNS.Transport.request_path(dest_hash)
            
            # Wait for path
            print("Waiting for path...")
            for i in range(10):
                time.sleep(1)
                if RNS.Transport.has_path(dest_hash):
                    break
            else:
                print("✗ Could not find path to destination")
                sys.exit(1)
                
        print("✓ Path to destination found")
        
        # Create Link to destination
        print("Establishing Link...")
        # Recall the server identity from the destination hash
        server_identity = RNS.Identity.recall(dest_hash)
        if server_identity is None:
            print("✗ Could not recall server identity")
            sys.exit(1)
            
        # Create destination object for linking
        server_destination = RNS.Destination(
            server_identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            "rserver", "web"
        )
        
        link = RNS.Link(server_destination)
        
        # Wait for Link establishment
        print("Waiting for Link establishment...")
        for i in range(10):
            time.sleep(1)
            if link.status == RNS.Link.ACTIVE:
                break
        else:
            print("✗ Link establishment failed")
            sys.exit(1)
            
        print("✓ Link established!")
        
        # Set up callback to receive responses
        def client_packet_received(data, packet):
            print(f"✓ Received response {len(data)} bytes: {data}")
            
        link.set_packet_callback(client_packet_received)
        
        # Send test message
        test_message = b"Hello from test client!"
        print(f"Sending {len(test_message)} bytes: {test_message}")
        packet = RNS.Packet(link, test_message)
        packet.send()
        
        # Wait for response
        print("Waiting for response...")
        time.sleep(2)
        
        # Close link
        link.teardown()
        print("✓ Link closed")
        
    except KeyboardInterrupt:
        print("\nTest client interrupted")
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()