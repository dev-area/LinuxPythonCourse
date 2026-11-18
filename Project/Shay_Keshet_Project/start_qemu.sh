#!/bin/bash

# Move to the QEMU directory
cd /home/liran/armsystem || exit 1

# Start QEMU
./run_qemu &
QEMU_PID=$!

# Wait for QEMU UART socket
while [ ! -S /tmp/qemu-uart ]; do
    sleep 1
done

# Connect UART
./setupuart &
UART_PID=$!

# Wait until QEMU exits
wait "$QEMU_PID"

# Stop UART connection
kill "$UART_PID" 2>/dev/null