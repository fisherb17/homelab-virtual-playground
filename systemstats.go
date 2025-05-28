package main

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"syscall"
)

func main() {
	printSystemStats()
}

func printSystemStats() {
	hostname, err := os.Hostname()
	if err != nil {
		hostname = "Unknown"
	}

	ipAddrs := getIPAddresses()

	osVersion := getOSVersion()

	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)

	fmt.Println("System Resource Report")
	fmt.Println("======================")
	fmt.Printf("Hostname:    %s\n", hostname)
	fmt.Printf("OS Version:  %s\n", osVersion)
	fmt.Println("IP Addresses:")
	for _, ip := range ipAddrs {
		fmt.Printf("  - %s\n", ip)
	}

	fmt.Printf("Go Routines: %d\n", runtime.NumGoroutine())
	fmt.Printf("CPU Cores:   %d\n", runtime.NumCPU())
	fmt.Printf("Memory Allocated: %.2f MB\n", float64(memStats.Alloc)/(1024*1024))
	fmt.Printf("Memory Sys:       %.2f MB\n", float64(memStats.Sys)/(1024*1024))

	fs := &syscall.Statfs_t{}
	err = syscall.Statfs(".", fs)
	if err == nil {
		total := fs.Blocks * uint64(fs.Bsize)
		free := fs.Bfree * uint64(fs.Bsize)
		fmt.Printf("Disk Total: %.2f GB\n", float64(total)/(1024*1024*1024))
		fmt.Printf("Disk Free:  %.2f GB\n", float64(free)/(1024*1024*1024))
	} else {
		fmt.Println("Disk stats not available.")
	}
}

func getIPAddresses() []string {
	var ips []string
	ifaces, err := net.Interfaces()
	if err != nil {
		return []string{"Unknown"}
	}
	for _, iface := range ifaces {
		addrs, err := iface.Addrs()
		if err != nil {
			continue
		}
		for _, addr := range addrs {
			var ip net.IP
			switch v := addr.(type) {
			case *net.IPNet:
				ip = v.IP
			case *net.IPAddr:
				ip = v.IP
			}
			// Skip loopback and IPv6 for simplicity
			if ip != nil && !ip.IsLoopback() && ip.To4() != nil {
				ips = append(ips, ip.String())
			}
		}
	}
	if len(ips) == 0 {
		ips = append(ips, "No non-loopback IPv4 address found")
	}
	return ips
}

func getOSVersion() string {
	out, err := exec.Command("uname", "-a").Output()
	if err != nil {
		return "Unknown"
	}
	return strings.TrimSpace(string(out))
}
