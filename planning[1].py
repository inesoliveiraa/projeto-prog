
def timeToMinutes(time):
    hours = int(time[:2])
    minutes = int(time[3:])
    return hours * 60 + minutes

def minutesToTime(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return str(hours).zfill(2) + "h" + str(mins).zfill(2)

def getServiceStatus(kms, autonomy, kmsUsed, accumulatedTime, startTime, endTime):
    remainingAutonomy = int(autonomy) - int(kmsUsed) - int(kms)

    accumulatedMinutes = timeToMinutes(accumulatedTime)
    serviceDuration = timeToMinutes(endTime) - timeToMinutes(startTime)
    totalMinutes = accumulatedMinutes + serviceDuration

    if remainingAutonomy < 15:
        return "charges"
    elif 300 - totalMinutes < 30:
        return "terminates"
    else:
        return "continues"

def updateServices(vehicles, reservations, waiting4Serv, waiting4Vehic):

    """
    Assigns drivers with their vehicles to services that were reserved.

    Requires:
    vehicles is dict with a structure as in the output of 
    getInfo.readVehiclesFile;
    reservations is list with a structure as in the output of 
    getInfo.readReservationsFile;
    waiting4Serv is list with the structure as in the output of
    getInfo.waiting4ServicesList; 
    waiting4Vehic is list with the structure as in the output of
    getInfo.waiting4VehiclesList;
    objects in reservations, waiting4Serv and waiting4Vehic
    concern the same 2 hour period p.
    Ensures:
    list of lists, where each list has the structure as in the
    output of getInfo.readServicesFile, representing the services 
    to be provided in period p upon having been reserved as they were input 
    in reservations.
    Reservations with earlier booking times are served first (lexicographic
    order of clients' names is used to resolve eventual ties).
    Drivers available earlier are assigned services first (lexicographic
    order of their names is used to resolve eventual ties) under 
    the following conditions:
    If a driver has less than 30 minutes left to reach their 5 hour 
    daily limit of accumulated activity, he is given no further service 
    in that day (with a service entry marked with "terminates") and 
    his vehicle is assigned to other driver yet with no vehicle, according 
    to the increasing hours of their arrival to the company (with another 
    service entry, marked with "standby");
    Else if a vehicle has less than 15 kms autonomy, it has to be recharged 
    (with a service entry marked with "charges") and is available 1 hour 
    later, after recharging (with another service entry, marked with 
    "standby");
    """

    reservationsOrdered = sorted(reservations, key=lambda r: (r[1], r[0]))
    
    services = []
    availableDrivers = [driver[:] for driver in waiting4Serv]
    
    for reservation in reservationsOrdered:
        client = reservation[0]
        startTime = reservation[1]
        endTime = reservation[2]
        circuit = reservation[3]
        kms = reservation[4]

        selectedDriver = None

        for driverInfo in availableDrivers:
            if timeToMinutes(driverInfo[4]) <= timeToMinutes(startTime):
                selectedDriver = driverInfo
                break

        if selectedDriver != None:
            driver = selectedDriver[1]
            plate = selectedDriver[0]
            accumulatedTime = selectedDriver[8]
            autonomy = selectedDriver[9]
            kmsUsed = selectedDriver[10]
            

            status = getServiceStatus(kms, autonomy, kmsUsed, accumulatedTime, startTime, endTime)

            services.append([plate, driver, client, startTime, endTime, circuit, kms, status])
            
            if status == "continues":
                selectedDriver[3] = startTime
                selectedDriver[4] = endTime
                selectedDriver[6] = kms
                selectedDriver[7] = status
                totalMinutes = timeToMinutes(accumulatedTime)
                serviceMinutes = timeToMinutes(endTime) - timeToMinutes(startTime)
                newTotal = totalMinutes + serviceMinutes

                selectedDriver[8] = str(newTotal // 60).zfill(2) + "h" + str(newTotal % 60).zfill(2)
                selectedDriver[10] = int(kmsUsed) + int(kms)
                
                
            elif status == "charges":
                availableDrivers.remove(selectedDriver)

            elif status == "terminates":
                availableDrivers.remove(selectedDriver)
        
    return services


def updateDrivers(services, drivers):
    """
    Provides an updated collection of drivers.

    Requires:
    services is list with a structure as in the output of 
    getInfo.updateServices representing the services for a 2 hour 
    period p;
    drivers is a dict with the structure as in the output of 
    getInfo.readDriversFile representing the drivers for the 2 hour 
    period immediately preceding period p.
    Ensures:
    dict of drivers updated with the information in services with 
    the structure as in the output of getInfo.readDriversFile 
    representing the drivers for the period p.
    """


def updateVehicles(services, vehicles):
    """
    <to be completed by students>
    """



