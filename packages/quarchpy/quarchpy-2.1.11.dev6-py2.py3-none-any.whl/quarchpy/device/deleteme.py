def list_network(target_conn="all", debugPring=False, lanTimeout=1, ipAddressLookup=None):

    ipList = socket.gethostbyname_ex(socket.gethostname())
    logging.debug(os.path.basename(__file__) + ": Discovered the following interfaces: " + str(ipList))
    for ip in ipList[2]:
        # Create and configure the socket for broadcast.
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        mySocket.settimeout(lanTimeout)

        lan_modules = dict()

        specifiedDevice = None

        if ipAddressLookup is not None:
            # Attempts to find the device through UDP then REST
            specifiedDevice = lookupDevice(str(ipAddressLookup).strip(), mySocket, lan_modules )



        # Broadcast the message.
        logging.debug("Broadcast LAN discovery message for UDP scan")
        mySocket.bind((ip,56732))
        mySocket.sendto(b'Discovery: Who is out there?\0\n', ('255.255.255.255', 36))
        #mySocket.sendto(b'Discovery: Who is out there?\0\n', ('255.255.255.255', 30303)) #56732

        counter = 0

        # Receive messages until timeout.
        while True:
            network_modules = {}
            counter += 1
            # Receive raw message until timeout, then break.
            try:
                msg_received = mySocket.recvfrom(256)
            except:
                # check if any a device was targeted directly and allow parse
                if specifiedDevice is not None:
                    msg_received = specifiedDevice
                    specifiedDevice = None
                else:
                    break
            cont = 0

            # print(msg_received)
            # Used split \r\n since values of 13 or 10 were looked at as /r and /n when using splitlines
            # This fixes for all cases except if 13 is followed by 10.
            splits = msg_received[0].split(b"\r\n")
            del splits[-1]
            for lines in splits:
                if cont <= 1:
                    index = cont
                    data = repr(lines).replace("'", "").replace("b", "")
                    cont += 1
                else:
                    index = repr(lines[0]).replace("'", "")
                    data = repr(lines[1:]).replace("'", "").replace("b", "")

                network_modules[index] = data

            module_name = get_user_level_serial_number(network_modules)
            logging.debug("Found UDP response: " + module_name)

            ip_module = msg_received[1][0].strip()

            try:
                # Add a QTL before modules without it.
                if "QTL" not in module_name.decode("utf-8"):
                    module_name = "QTL" + module_name.decode("utf-8")
            except:
                # Add a QTL before modules without it.
                if "QTL" not in module_name:
                    module_name = "QTL" + module_name

            # Checks if there's a value in the TELNET key.
            if (target_conn.lower() == "all" or target_conn.lower() == "telnet"):
                if network_modules.get("\\x8a") or network_modules.get("138"):
                    # Append the information to the list.
                    lan_modules["TELNET:" + ip_module] = module_name
                    logging.debug("Found Telnet module: " + module_name)

            # Checks if there's a value in the REST key.
            if (target_conn.lower() == "all" or target_conn.lower() == "rest"):
                if network_modules.get("\\x84") or network_modules.get("132"):
                    # Append the information to the list.
                    lan_modules["REST:" + ip_module] = module_name
                    logging.debug("Found REST module: " + module_name)

            # Checks if there's a value in the TCP key.
            if (target_conn.lower() == "all" or target_conn.lower() == "tcp"):
                if network_modules.get("\\x85") or network_modules.get("133"):
                    # Append the information to the list.
                    lan_modules["TCP:" + ip_module] = module_name
                    logging.debug("Found TCP module: " + module_name)

        mySocket.close()
        logging.debug("Finished UDP scan")

    retVal+=lan_modules
    return retVal