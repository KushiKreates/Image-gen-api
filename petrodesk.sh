un_system() {
  #!/bin/bash

    #!/bin/bash

echo "   ___   _____________  ___   __      _______   ____  __  _____    _   ____  _______  "
echo "  / _ | / __/_  __/ _ \/ _ | / / ____/ ___/ /  / __ \/ / / / _ \  | | / /  |/  / __/  "
echo " / __ |_\ \  / / / , _/ __ |/ /_/___/ /__/ /__/ /_/ / /_/ / // /  | |/ / /|_/ /\ \    "
echo "/_/ |_/___/ /_/ /_/|_/_/ |_/____/   \___/____/\____/\____/____/   |___/_/  /_/___/    "
echo ""
echo "========================================================="
echo "  POWERED by nulldaemon's Petrodesk,(Kushi_k)"
echo "========================================================="
echo ""
echo "========================================================="
echo "  HOW TO USE MY VIRTUAL MACHINE?"
echo "========================================================="
echo "Please head over to $(curl https://checkip.pterodactyl-installer.se/ 2>/dev/null):$SERVER_PORT"
echo "and use server ID as the password."
echo ""
echo "========================================================================================"
echo "©️ 2024, Astral-Cloud (The best hosting provider!)"


  # abort if file
  if [ -f "$HOME/.do-not-start" ]; then
    rm -rf "$HOME/.do-not-start"
    cp /etc/resolv.conf "$install_path/etc/resolv.conf" -v
    $DOCKER_RUN /bin/sh
    exit
  fi
  # Starting NoVNC
  $install_path/dockerd --kill-on-exit -r $install_path -b /dev -b /proc -b /sys -b /tmp -w "/usr/lib/noVNC" /bin/sh -c \
    "./utils/novnc_proxy --vnc localhost:5901 --listen 0.0.0.0:$SERVER_PORT --cert self.crt --key self.key --ssl-only" &>/dev/null &

  # Set up VNCPasswd
  chmod 0600 "$install_path$HOME/.vnc/passwd" # prerequisite

  $DOCKER_RUN "export PATH=$install_path/bin:$install_path/usr/bin:$PATH HOME=$install_path$HOME LD_LIBRARY_PATH='$install_path/usr/lib:$install_path/lib:/usr/lib:/usr/lib64:/lib64:/lib'; \
    cd $install_path$HOME; \
    export MOZ_DISABLE_CONTENT_SANDBOX=1 \
    MOZ_DISABLE_SOCKET_PROCESS_SANDBOX=1 \
    MOZ_DISABLE_RDD_SANDBOX=1 \
    MOZ_DISABLE_GMP_SANDBOX=1 \
    HOME='$install_path$HOME' \
    HOSTNAME=pterodesk; \
    $(if_x86_64 "vglrun -d egl") vncserver :0" &>/dev/null
}
