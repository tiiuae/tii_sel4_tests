def upload(boot_image_path, hostname, tftpboot):
    import sys
    from paramiko import SSHClient
    from scp import SCPClient

    def progress(filename, size, sent):
        sys.stdout.write("\r%s\'s progress: %.2f%%   " % (filename, float(sent)/float(size)*100))

    if not boot_image_path:
        return
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname)

    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport(), progress = progress)

    #TODO: unhardcode remote_path
    scp.put(boot_image_path, remote_path=tftpboot)
    print("")

    scp.close()
