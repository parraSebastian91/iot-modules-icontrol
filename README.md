# iot-modules-icontrol

CONSTANTES DE CONFIGURACIÓN

ID_DISPOSITIVO = ""
GRUPO_RECURSO = ""
LOCACION = ""
HUB_NAME = ""
CON_STRING_DEVICE = ""
CON_STRING_SERVICE = ""
===========================================

# Se crea una extencion en la CLI de Azure
- az extension add --upgrade --name azure-iot

# se crea un grupo de recursos en una locacion especifica
- az group create --name {GRUPO_RECURSO} --location {{LOCACION}}

# Crea una instancia de IoT Hub. 
- az iot hub create --resource-group {GRUPO_RECURSO} --name {HUB_NAME}

# Obtener ConnectionString del IoT HUB
- az iot hub connection-string  show --hub-name icontrolo-id-01
{HUB_NAME}
icontrolo-id-01


# Registrar un Dispositivo
- az iot hub device-identity create --device-id {ID_DISPOSITIVO} --hub-name {HUB_NAME}

# Obtener ConnectionString de disposibtivo
- az iot hub device-identity connection-string show --device-id {ID_DISPOSITIVO} --hub-name {HUB_NAME}

# Obtener conection string del servicio HUB IOT
- az iot hub connection-string show --policy-name service --hub-name {HUB_NAME} --output table

# Luego exportar las variables en el sistema operativo donde este alojado el codigo de ejecucion

export IOTHUB_DEVICE_CONNECTION_STRING="{CON_STRING}"
export IOTHUB_DEVICE_SECURITY_TYPE="connectionString"

# Ejecutar codigo en el dispositivo

# Ver Telemetria a travez de CLI 
- az iot hub monitor-events --output table --device-id {ID_DISPOSITIVO} --hub-name {HUB_NAME}

=================================================

Instalacion IOT Edge en dispositivo 
*URL(https://learn.microsoft.com/es-es/azure/iot-edge/how-to-provision-single-device-linux-symmetric?view=iotedge-1.4&tabs=azure-portal%2Cdebian)
- La creacion de este dispositivo tiene que ser en IOT EDGE
#Instalacion de paquetes de Microsoft
- curl https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb > ./packages-microsoft-prod.deb
- sudo apt install ./packages-microsoft-prod.deb
#Instalacion del motor de contenedores Docker Moby-Engine
- sudo apt-get update
- sudo apt-get install moby-engine
# Verificaciones de configuracon Daemon
- cd /etc/docker
# Crear Archivo ".json" si no existe
- Nombre archivo "daemon.json"
  Contenido:
   {
      "log-driver": "local"
   }
# Reiniciar servicio Docker
- sudo systemctl restart docker

Instalacion entorno de ejecucion de IOT Edge
- sudo apt-get update
- sudo apt-get install aziot-edge defender-iot-micro-agent-edge

# Provicionamiento de dispositivo <<<< Aqui empieza la configuracion del EQUIPO IOT
- sudo iotedge config mp --connection-string {CON_STRING_DEVICE}
// sudo iotedge config mp --connection-string "HostName=raspBerry-icontrolo1.azure-devices.net;DeviceId=icontrolo-rbp4-v01;SharedAccessKey=H/T9a8+IbDt9SCkl2jPKjenIOxYcBeGLr0gnU43fe9g="
# Aplicar configuracion
- sudo iotedge config apply -c '/etc/aziot/config.toml'

implementacion de modulos en el dispositivo
  1. Seleccione Dispositivos en el menú IoT Hub.
  2. Seleccione el dispositivo para abrir su página.
  3. Seleccione la pestaña Establecer módulos .
  4. Puesto que queremos implementar el IoT Edge módulos predeterminados (edgeAgent y edgeHub), no es necesario agregar ningún módulo a este panel, por lo que seleccione Revisar y crear en la parte inferior.
  5. Verá la confirmación JSON de los módulos. Seleccione Crear para implementar los módulos.
  
# Comporbacion de configuracion Correcta
- sudo iotedge system status
# Logs de servicio
- sudo iotedge system logs
# comprobar el estado de la configuración y la conexión del dispositivo.
- sudo iotedge check

Creacion de Modulo Personalizado
# Instalar extensiones VsCode
- Azure IoT Edge y Azure IoT Hub.
# Iniciar sesion azure en VsCode
- ctrl + shift + p luego "Azure: sign in"
# antes crear un contenedor en Azure Container Registry
# Crear un modulo IoT Edge con el servicio de contenedores de Azure Container Registry
- ctrl + shift + p "Azure IoT Edge: New IoT Edge solution"
# una ves programado el modulo se ingresa al contenedor Docker
(USUARIO) = icontrolorbp1
(PASS) = FnJKsfD4oHdcBnGiVMGChKF2pnYS4EQDOHNRtbs6b4+ACRAJ/WwJ
(SERVICIO) = icontrolorbp1.azurecr.io
docker login -u <ACR username> -p <ACR password> <ACR login server>
sudo docker login -u icontrolorbp1 -p FnJKsfD4oHdcBnGiVMGChKF2pnYS4EQDOHNRtbs6b4+ACRAJ/WwJ icontrolorbp1.azurecr.io

docker login -u PerimeterSolution -p JwjraZyEK4Try3V+eddbl72KeBrbBFao9xXwDVC7Lf+ACRCaNTJ8 perimetersolution.azurecr.io



