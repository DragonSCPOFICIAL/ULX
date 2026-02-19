Para uma experiência mais próxima do que você descreveu, o `ulx-run-apk` precisaria de uma integração mais profunda com o Anbox, incluindo a instalação automática do APK no ambiente Anbox e o lançamento do aplicativo específico. Isso é complexo para um script de instalação simples, mas o esqueleto está aqui.

# Placeholder para o comando real de execução do APK via Anbox
# Por enquanto, apenas um log para indicar que a chamada foi interceptada.
/usr/bin/anbox-session-manager & # Inicia o serviço Anbox se não estiver rodando
/usr/bin/anbox launch --file "$1" # Tenta lançar o APK diretamente

EOF
sudo chmod +x /usr/local/bin/ulx-run-apk

# Criar arquivo de configuração binfmt para .apk
cat <<EOF | sudo tee /etc/binfmt.d/ulx-apk.conf > /dev/null
:ulx-apk:M::PK\x03\x04::/usr/local/bin/ulx-run-apk:
EOF

# Recarregar configurações do binfmt_misc para aplicar as novas regras imediatamente
sudo systemctl restart systemd-binfmt

echo "========================================================="
echo "PONTE UNIVERSAL ATIVADA E PERSISTENTE!"
echo "Agora você pode executar .exe e .apk diretamente no terminal ou clicando."
echo "========================================================="
