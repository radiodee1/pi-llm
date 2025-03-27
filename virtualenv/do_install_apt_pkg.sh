sudo apt install python3-dotenv python3-pyaudio portaudio19-dev python3-espeak python3-mesonpy libcairo2-dev libgirepository1.0-dev libsqlite3-dev libghc-setenv-dev  gcc make gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu qemu-system-arm qemu-user-static -y

echo ""
echo "NOTE: you may need to start qemu-system-arm to enable cross compiling."
echo "$ sudo systemctl restart systemd-binfmt.service"
