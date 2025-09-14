#!/usr/bin/env python3
"""
MeshCurl - HTTP client for Reticulum networks, like curl over mesh.
"""

import RNS
import sys
import time
import argparse


def main():
    parser = argparse.ArgumentParser(description="MeshCurl - HTTP client for Reticulum networks")
    parser.add_argument("destination", help="Server destination hash")
    parser.add_argument("-X", "--request", default="GET", help="HTTP method (default: GET)")
    parser.add_argument("path", nargs="?", default="/", help="Path to request (default: /)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print("MeshCurl - HTTP over Reticulum")
    print("=" * 30)
    
    destination_hash = args.destination
    method = args.request.upper()
    path = args.path if args.path.startswith('/') else '/' + args.path
    
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
            print(f"✓ Received HTTP response ({len(data)} bytes):")
            try:
                response_text = data.decode('utf-8')
                print(response_text)
            except UnicodeDecodeError:
                print(f"Binary data: {data}")
            
        link.set_packet_callback(client_packet_received)
        
        # Send HTTP request like curl
        http_request = f"{method} {path} HTTP/1.1\r\nHost: {destination_hash}\r\nUser-Agent: MeshCurl/1.0\r\nAccept: text/html,*/*\r\n\r\n"
        test_message = http_request.encode('utf-8')
        
        if args.verbose:
            print(f"Sending HTTP request ({len(test_message)} bytes):")
            print(http_request)
        else:
            print(f"Requesting: {method} {path}")
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