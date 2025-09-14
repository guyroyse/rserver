#!/usr/bin/env python3

import RNS
import sys
import time

import config
from identity import get_or_create_identity
from destination import create_destination

def main():
    print("RServer - Reticulum Web Server")
    print("=" * 40)
    
    print("Initializing Reticulum...")
    
    try:
        # Initialize Reticulum with default config
        reticulum = RNS.Reticulum()
        print("✓ Reticulum initialized successfully")
        
        # Display basic status using correct API
        print(f"✓ Transport enabled: {RNS.Reticulum.transport_enabled()}")
        print(f"✓ Instance ready: {RNS.Reticulum.get_instance() is not None}")
        print(f"✓ Public directory: {config.public_dir()}")
        
        # Load or create server identity
        identity, was_created = get_or_create_identity()
        if was_created:
            print("✓ Created new server identity")
        else:
            print("✓ Loaded existing server identity")

        print(f"✓ Identity hash: {RNS.prettyhexrep(identity.hash)}")
        
        # Create destination for this server
        destination = create_destination(identity)
        app_name, aspect = config.app_context()

        print(f"✓ Server destination: {RNS.prettyhexrep(destination.hash)}")
        print(f"✓ App context: {app_name}.{aspect}")

        # Start the web server        
        print("\nReticulum is running. Press Ctrl+C to exit.")
        
        # Keep the program running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down RServer...")
        RNS.exit()
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ Error initializing Reticulum: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()