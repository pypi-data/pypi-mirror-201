#!/usr/bin/env python
import argparse

def start_vms(num_vms):
    print(f'Starting {num_vms} GCP VMs')
    # 實現啟動 GCP VM 的功能

def stop_vms(vm_ids):
    print(f'Stopping GCP VMs: {", ".join(vm_ids)}')
    # 實現停止 GCP VM 的功能

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GCP VM 管理器")
    parser.add_argument('--action', type=str, required=True, choices=['start', 'stop'], help="要執行的操作")
    parser.add_argument('--num_vms', type=int, help="要啟動的 GCP VM 數量")
    parser.add_argument('--vm_ids', nargs='*', help="要停止的 GCP VM ID")
    args = parser.parse_args()

    if args.action == "start":
        if not args.num_vms:
            parser.error("啟動 GCP VM 時需要提供 --num_vms 參數")
        start_vms(args.num_vms)
    elif args.action == "stop":
        if not args.vm_ids:
            parser.error("停止 GCP VM 時需要提供 --vm_ids 參數")
        stop_vms(args.vm_ids)
