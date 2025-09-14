#!/usr/bin/env python3

import RNS
import sys
import time

import config
from identity import get_or_create_identity
from destination import create_destination
from content import ensure_public_directory

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

        # Load or create server identity
        identity, was_created = get_or_create_identity()
        print(f"✓ {'Created' if was_created else 'Loaded'} server identity: {RNS.prettyhexrep(identity.hash)}")
        
        # Create destination for this server
        destination = create_destination(identity)
        app_name, aspect = config.app_context()

        print(f"✓ Server destination: {RNS.prettyhexrep(destination.hash)}")
        print(f"✓ App context: {app_name}.{aspect}")

        # Ensure public directory exists with default content
        print(f"✓ Public directory: {config.public_dir()}")

        created = ensure_public_directory()
        if created:
            print(f"✓ Created public directory: {config.public_dir()}")
            print(f"✓ Created default file: {config.default_file()}")

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