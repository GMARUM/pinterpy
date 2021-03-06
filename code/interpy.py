# -*- coding: utf-8 -*-
"""
EPS. 01 Feb 2019.
"""
def interpy():
    
    import sys, os
    from netCDF4 import Dataset
    from wrf import getvar, vinterp
    from ast import literal_eval
    import numpy as np
    import xarray
    
    interpnamelist = sys.argv[1] 

    if '/' in interpnamelist:
        interpnamelistpath = interpnamelist.replace(interpnamelist.split('/')[-1],'')
        listfilesnamelistpath = []
        for (dirpath, dirnames, filenames) in os.walk(interpnamelistpath, topdown=True):
            listfilesnamelistpath.extend(filenames)
            del dirnames[:]
    if '/' not in interpnamelist:
        listfilesnamelistpath = []
        pwdd=os.getcwd()
        for (dirpath, dirnames, filenames) in os.walk(pwdd, topdown=True):
            listfilesnamelistpath.extend(filenames)
            del dirnames[:]
        
    
    if (interpnamelist.split('/')[-1] not in listfilesnamelistpath): 
       print('Provided namelist could not be found. Please verify its location.')
       return
        
    cont=[]
    with open(interpnamelist) as g:
         for line in g:
             cont.append(line.strip())

    #input file 
    if sum(["ncinputfile" in aa for aa in cont]) == 1: 
       booleanvec = np.array(["ncinputfile" in aa for aa in cont])
       inputfileline = str((np.array(cont)[booleanvec])[0])  
       ncinputfile = literal_eval(inputfileline.split('=')[-1])
    
       if '/' in ncinputfile:
        inputfilepath = ncinputfile.replace(ncinputfile.split('/')[-1],'')
        listfilesinputpath = []
        for (dirpath, dirnames, filenames) in os.walk(inputfilepath, topdown=True):
            listfilesinputpath.extend(filenames)
            del dirnames[:]
       if '/' not in ncinputfile:
        listfilesinputpath = []
        pwdd=os.getcwd()
        for (dirpath, dirnames, filenames) in os.walk(pwdd, topdown=True):
            listfilesinputpath.extend(filenames)
            del dirnames[:]
        
       if (ncinputfile.split('/')[-1] not in listfilesinputpath): 
           print('Provided input file could not be found. Please verify its location.')
           return
              
    if sum(["ncinputfile" in aa for aa in cont]) == 0:
        print("No input file was provided")
        return
    if sum(["ncinputfile" in aa for aa in cont]) > 1:
        print("More than one input file was provided")
        return
    
    
    #plevels
    if sum(["plevels" in aa for aa in cont]) == 1: 
       booleanvec = np.array(["plevels" in aa for aa in cont])
       plevelsline = str((np.array(cont)[booleanvec])[0])
       plevels = literal_eval(plevelsline.split('=',1)[-1])
       if plevels == None:
          plevels = [1000.0,900.0,800.0,700.0,600.0,500.0,400.0,300.0]
          print("No pressure levels were given to interpolate. The next default levels will be used: ", plevels, "hPa")
    if sum(["plevels" in aa for aa in cont]) == 0:
       plevels = [1000.0,900.0,800.0,700.0,600.0,500.0,400.0,300.0]
       print("No pressure levels were given to interpolate. The next default levels will be used: ", plevels, "hPa")
       return
    if sum(["plevels" in aa for aa in cont]) > 1:
       plevels = [1000.0,900.0,800.0,700.0,600.0,500.0,400.0,300.0]
       print("More than one pressure levels vector was provided. The next default levels will be used: ", plevels, " hPa")
       return
    
    #fields to interpolate 
    if sum(["getfield" in aa for aa in cont]) == 1: 
       booleanvec = np.array(["getfield" in aa for aa in cont])
       interpfieldfileline = str((np.array(cont)[booleanvec])[0])
       interpfield = literal_eval(interpfieldfileline.split('=')[-1])
    if sum(["getfield" in aa for aa in cont]) == 0:
        print("No field to interpolate was provided")
        return
    if sum(["getfield" in aa for aa in cont]) > 1:
        print("More than one field to interpolate was provided")
        return
    
    if type(interpfield) == str:
        interpfieldlist = interpfield.split()
    if type(interpfield) == list:
        interpfieldlist = interpfield
        
        
    #units of the field to interpolate
    if len(interpfieldlist) == 1:
        if sum(["fieldunits" in aa for aa in cont]) == 1:
           booleanvec = np.array(["fieldunits" in aa for aa in cont])
           fieldunitsline = str((np.array(cont)[booleanvec])[0])
           fieldunits = literal_eval(fieldunitsline.split('=')[-1])
           if fieldunits == None:
              print("No units were provided for the fields to interpolate. Default units will be used.")
              fieldunitslist=[None]
           else:
               fieldunitslist=[fieldunits]
        if sum(["fieldunits" in aa for aa in cont]) == 0:
           fieldunitslist=[None]
           print("No units were provided for the fields to interpolate. Default units will be used.")
        if sum(["fieldunits" in aa for aa in cont]) > 1:
            fieldunitslist=[None]
            print("More than one units for the fields to interpolate were provided. Default units will be used.")
            
    if len(interpfieldlist) > 1:
        if sum(["fieldunits" in aa for aa in cont]) == 1:
           booleanvec = np.array(["fieldunits" in aa for aa in cont])
           fieldunitsline = str((np.array(cont)[booleanvec])[0])
           fieldunits = literal_eval(fieldunitsline.split('=')[-1])
           if fieldunits == None:
              print("No units vector was provided for the fields to interpolate. Default units will be used.")
              fieldunitslist=[None for aa in interpfieldlist]
           else:
               if type(fieldunits) is not list:
                   fieldunits = fieldunits.split()
               if len(fieldunits) != len(interpfieldlist):
                   fieldunitslist = [None for aa in interpfieldlist]
               if len(fieldunits) == len(interpfieldlist):
                   fieldunitslist = fieldunits
        if sum(["fieldunits" in aa for aa in cont]) == 0:
           fieldunitslist = [None for aa in interpfieldlist]
           print("No units vector was provided for the fields to interpolate. Default units will be used.")
        if sum(["fieldunits" in aa for aa in cont]) > 1:
            fieldunitslist = [None for aa in interpfieldlist]
            print("More than one units vector for the fields to interpolate was provided. Default units will be used.")
            
        
    #output file     
    if len(interpfieldlist) == 1:
        if sum(["ncoutputfile" in aa for aa in cont]) == 1: 
           booleanvec = np.array(["ncoutputfile" in aa for aa in cont])
           outputfilenameline = str((np.array(cont)[booleanvec])[0])
           ncoutputfile = literal_eval(outputfilenameline.split('=')[-1])
           if ncoutputfile == None:
               ncoutputfilelist = ncinputfile.split('/')[-1] + '-interp-' + interpfieldlist[0] + '.nc'
           else:
               if '/' in ncoutputfile:
                outputfilepath = ncoutputfile.replace(ncinputfile.split('/')[-1],'')
                listfilesoutputpath = []
                for (dirpath, dirnames, filenames) in os.walk(outputfilepath, topdown=True):
                    listfilesoutputpath.extend(filenames)
                    del dirnames[:]
               if '/' not in ncoutputfile:
                listfilesoutputpath = []
                pwdd=os.getcwd()
                for (dirpath, dirnames, filenames) in os.walk(pwdd, topdown=True):
                    listfilesoutputpath.extend(filenames)
                    del dirnames[:]
                
               if (ncoutputfile.split('/')[-1] in listfilesinputpath): 
                   outputfileover=input('There already exists a file with the name provided for the output file. Please type whether the existing file should be overwritten [y] or not [n] here >>> ')
                   if outputfileover == 'n':
                       newoutputfilename=input('Press ENTER to use the default output name or type an alternate name for the output file >>> ')
                       if len(newoutputfilename) == 0:
                          ncoutputfile = (ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + interpfieldlist[0] + '.nc'              
                       if len(newoutputfilename)  > 0:
                          ncoutputfile=newoutputfilename
        
        if sum(["ncoutputfile" in aa for aa in cont]) == 0:
            print("No output file name was provided. Default name will be used for the output file.")
            ncoutputfile = (ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + interpfieldlist[0] + '.nc'
        if sum(["ncoutputfile" in aa for aa in cont]) > 1:
            print("More than one output file name was provided. Default name will be used for the output file.")
            ncoutputfile = (ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + interpfieldlist[0] + '.nc'
        
        ncoutputfilelist = ncoutputfile.split()
                      
    if len(interpfieldlist) > 1:
        if sum(["ncoutputfile" in aa for aa in cont]) == 1: 
           booleanvec = np.array(["ncoutputfile" in aa for aa in cont])
           outputfilenameline = str((np.array(cont)[booleanvec])[0])
           ncoutputfile = literal_eval(outputfilenameline.split('=')[-1])
           if ncoutputfile == None:
               ncoutputfilelist = [((ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + abc + '.nc') for abc in interpfieldlist]
           else:
               if type(ncoutputfile) is not list:
                   ncoutputfile = ncoutputfile.split()
               if len(ncoutputfile) == 1:
                  print('Single output file name was provided for the requested multiple fields to interpolate. Given output name will be used as prefix for the multiple output files names.')
                  ncoutputfilelist = [(((ncoutputfile[0]).split('/')[-1]).replace('.nc','') + '-' + abc + '.nc') for abc in interpfieldlist]
               if len(ncoutputfile) > 1:
                  if len(ncoutputfile) != len(interpfieldlist):
                     print('Not enough output file names were provided for the requested fields to interpolate. Default names will be used for the output files names.')
                     ncoutputfilelist = [((ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + abc + '.nc') for abc in interpfieldlist]
                  if len(ncoutputfile) == len(interpfieldlist):
                     ncoutputfilelist = ncoutputfile
                      
        if sum(["ncoutputfile" in aa for aa in cont]) == 0:
            print("No output file name was provided. Default names will be used for the output files names.")
            ncoutputfilelist = [((ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + abc + '.nc') for abc in interpfieldlist]                      
                   
        if sum(["ncoutputfile" in aa for aa in cont]) > 1:
            print("More than one output file name was provided. Default name will be used for the output file.")
            ncoutputfilelist = [((ncinputfile.split('/')[-1]).replace('.nc','') + '-interp-' + abc + '.nc') for abc in interpfieldlist]                    
                    
    #interpolate
    if len(interpfieldlist) == 1:
        if sum(["interpolate" in aa for aa in cont]) == 1: 
           booleanvec = np.array(["interpolate" in aa for aa in cont])
           interppline = str((np.array(cont)[booleanvec])[0])
           interppfield = literal_eval(interppline.split('=')[-1])
           if interppfield == False:
              print("No interpolation option was provided. Thus, no interpolation will be performed.")
              interppfieldlist=[False]
           if interppfield == True:
              interppfieldlist=[True]
           else:
              interppfieldlist=[False]
        if sum(["interpolate" in aa for aa in cont]) == 0:
            print("No interpolation option was provided. Thus, no interpolation will be performed.")
            interppfieldlist=[False]
        if sum(["interpolate" in aa for aa in cont]) > 1:
            print("More than one interpolation option was provided. Thus, no interpolation will be performed.")
            interppfieldlist=[False]
            
    if len(interpfieldlist) > 1:
        if sum(["interpolate" in aa for aa in cont]) == 1:
           booleanvec = np.array(["interpolate" in aa for aa in cont])
           interppline = str((np.array(cont)[booleanvec])[0])
           interppfield = literal_eval(interppline.split('=')[-1])
           if type(interppfield) is not list:
               if interppfield == False:
                  print("Single interpolation option was provided for multiple fields to interpolate. The specified 'False' option will be used for them all.")
                  interppfieldlist=[False for aa in interpfieldlist]
               if interppfield == True:
                  print("Single interpolation option was provided for multiple fields to interpolate. The specified 'True' option will be used for them all.")
                  interppfieldlist=[True for aa in interpfieldlist]
           else:
               if len(interppfield) != len(interpfieldlist):
                   print("Less interpolation options than fields to interpolate were provided. The default 'False' option will be used for them all.")
                   interppfieldlist = [False for aa in interpfieldlist]
               if len(interppfield) == len(interpfieldlist):
                   interppfieldlist = interppfield
        if sum(["interpolate" in aa for aa in cont]) == 0:
            print("No interpolation option was provided. Thus, no interpolation will be performed.")
            interppfieldlist = [False for aa in interpfieldlist]
        if sum(["interpolate" in aa for aa in cont]) > 1:
            print("More than one interpolation option was provided. Thus, no interpolation will be performed.")
            interppfieldlist = [False for aa in interpfieldlist]                       
                    
    #extrapolate
    if len(interpfieldlist) == 1:
        if sum(["extrapolate" in aa for aa in cont]) == 1: 
           booleanvec = np.array(["extrapolate" in aa for aa in cont])
           extrapline = str((np.array(cont)[booleanvec])[0])
           extrapfield = literal_eval(extrapline.split('=')[-1])
           if extrapfield == False:
              print("No extrapolation option was provided. Thus, no extrapolation will be performed.")
              extrapfieldlist=[False]
           if extrapfield == True:
              extrapfieldlist=[True]
           else:
              extrapfieldlist=[False]
        if sum(["extrapolate" in aa for aa in cont]) == 0:
            print("No extrapolation option was provided. Thus, no extrapolation will be performed.")
            extrapfieldlist=[False]
        if sum(["extrapolate" in aa for aa in cont]) > 1:
            print("More than one extrapolation option was provided. Thus, no extrapolation will be performed.")
            extrapfieldlist=[False]
            
    if len(interpfieldlist) > 1:
        if sum(["extrapolate" in aa for aa in cont]) == 1:
           booleanvec = np.array(["extrapolate" in aa for aa in cont])
           extrapline = str((np.array(cont)[booleanvec])[0])
           extrapfield = literal_eval(extrapline.split('=')[-1])
           if type(extrapfield) is not list:
               if extrapfield == False:
                  print("Single extrapolation option was provided for multiple fields to interpolate. The specified 'False' option will be used for them all.")
                  extrapfieldlist=[False for aa in interpfieldlist]
               if extrapfield == True:
                  print("Single extrapolation option was provided for multiple fields to interpolate. The specified 'True' option will be used for them all.")
                  extrapfieldlist=[True for aa in interpfieldlist]
           else:
               if len(extrapfield) != len(interpfieldlist):
                   print("Less extrapolation options than fields to interpolate were provided. The default 'False' option will be used for them all.")
                   extrapfieldlist = [False for aa in interpfieldlist]
               if len(extrapfield) == len(interpfieldlist):
                   extrapfieldlist = extrapfield
        if sum(["extrapolate" in aa for aa in cont]) == 0:
            print("No extrapolation option was provided. Thus, no extrapolation will be performed.")
            extrapfieldlist = [False for aa in interpfieldlist]
        if sum(["extrapolate" in aa for aa in cont]) > 1:
            print("More than one extrapolation option was provided. Thus, no extrapolation will be performed.")
            extrapfieldlist = [False for aa in interpfieldlist]             
            
            
   
                    
                    
    ncfile = Dataset(ncinputfile)
    variables=[aa for aa in ncfile.variables]
    print('Imported ', len(variables)-3, 'variables')
    #yn = input('Do you want to see them all? [y/n] >>> ')
    #if yn == 'y':
    #   print(ncfile.variables)     

        
    dimsnames = [aa for aa in ncfile.dimensions]
    
    if 'Time' not in dimsnames:
        print('Single time step was found in the input file')

        for i in range(0,len(interpfieldlist)):
            
            interpfield = interpfieldlist[i]
            ncoutputfile = ncoutputfilelist[i]
            fieldunits = fieldunitslist[i]  
            interpoption = interppfieldlist[i]
            extrapfield = extrapfieldlist[i]

            corrfields=['pressure','pres','p','pressure_hpa','pres_hpa','p_hpa','z','ght','z_km','ght_km','tc','tk','theta','th','theta_e','thetae','eth']
            fieldtypes=['pressure','pres','p','pressure_hpa','pres_hpa','p_hpa','z','ght','z_km','ght_km','tc','tk','theta','th','theta-e','thetae','eth']
            if interpfield not in corrfields:
               fieldtype='none'
            else:
               fieldtype=fieldtypes[corrfields.index(interpfield)]

            
             
            
            print('Calculating ', interpfield, ' ...')
            if fieldunits == None:
               interpvar = getvar(ncfile, interpfield, timeidx=None)
            else:
               interpvar = getvar(ncfile, interpfield, timeidx=None, units=fieldunits)
    
        
            if ('bottom_top' in interpvar.dims) == False:
                plevelsinterpolatedfield = interpvar
                if ('u_v' in interpvar.dims) == True:
                        plevelsinterpolatedfieldU = interpvar.isel(u_v=0)
                        plevelsinterpolatedfieldV = interpvar.isel(u_v=1)
                        plevelsinterpolatedfieldMOD = np.sqrt(plevelsinterpolatedfieldU*plevelsinterpolatedfieldU + plevelsinterpolatedfieldV*plevelsinterpolatedfieldV)
                if interpoption==True:
                    print('Warning: interpolation is not an appliable method for single-level fields, and hence it will not be performed.')
            if ('bottom_top' in interpvar.dims) == True:
                if interpoption==True:
                    print('Interpolating ', interpfield,' to ', len(plevels), ' pressure levels ...')
                    if ('u_v' in interpvar.dims) == True:
                        plevelsinterpolatedfieldU = vinterp(ncfile, field=interpvar.isel(u_v=0), vert_coord="pressure", 
                                                           interp_levels=plevels, timeidx=None,extrapolate=extrapfield)
                        plevelsinterpolatedfieldV = vinterp(ncfile, field=interpvar.isel(u_v=1), vert_coord="pressure", 
                                                           interp_levels=plevels, timeidx=None,extrapolate=extrapfield)
                        plevelsinterpolatedfieldMOD= np.sqrt(plevelsinterpolatedfieldU*plevelsinterpolatedfieldU + plevelsinterpolatedfieldV*plevelsinterpolatedfieldV)
                    else:
                        if interpfield=='z':
                           plevelsinterpolatedfield = vinterp(ncfile, field=interpvar, vert_coord="pressure", field_type='z',log_p=True,
                                                       interp_levels=plevels, timeidx=None,extrapolate=extrapfield)
                        else:
                           plevelsinterpolatedfield = vinterp(ncfile, field=interpvar, vert_coord="pressure", field_type=fieldtype,log_p=True,
                                                       interp_levels=plevels, timeidx=None,extrapolate=extrapfield)   
                    print('Interpolation of ', interpfield,' to pressure levels completed successfully')
                if interpoption==False:
                    plevelsinterpolatedfield = interpvar
    
            #Export to netCDF:
            if ('u_v' in interpvar.dims) == True:
                ncoutputfileU = ncoutputfile.replace('.nc','') + '-U.nc'
                del plevelsinterpolatedfieldU.attrs['coordinates']
                plevelsinterpolatedfieldU.attrs['projection'] = str(plevelsinterpolatedfieldU.projection)
                plevelsinterpolatedfieldU.XLONG.attrs['units'] = 'degrees_east'
                plevelsinterpolatedfieldU.XLAT.attrs['units'] = 'degrees_north' 
                plevelsinterpolatedfieldU.to_netcdf(ncoutputfileU) 
                ncoutputfileV = ncoutputfile.replace('.nc','') + '-V.nc'
                del plevelsinterpolatedfieldV.attrs['coordinates']
                plevelsinterpolatedfieldV.attrs['projection'] = str(plevelsinterpolatedfieldV.projection)
                plevelsinterpolatedfieldV.XLONG.attrs['units'] = 'degrees_east'
                plevelsinterpolatedfieldV.XLAT.attrs['units'] = 'degrees_north'
                plevelsinterpolatedfieldV.to_netcdf(ncoutputfileV)
                ncoutputfileMOD = ncoutputfile.replace('.nc','') + '-MOD.nc'
                plevelsinterpolatedfieldMOD.XLONG.attrs['units'] = 'degrees_east'
                plevelsinterpolatedfieldMOD.XLAT.attrs['units'] = 'degrees_north'
                plevelsinterpolatedfieldMOD.to_netcdf(ncoutputfileMOD)     
            else:
                del plevelsinterpolatedfield.attrs['coordinates']
                plevelsinterpolatedfield.attrs['projection'] = str(plevelsinterpolatedfield.projection)
                plevelsinterpolatedfield.XLONG.attrs['units'] = 'degrees_east'
                plevelsinterpolatedfield.XLAT.attrs['units'] = 'degrees_north'
                plevelsinterpolatedfield.to_netcdf(ncoutputfile) 

      
    if 'Time' in dimsnames:
        print(len(ncfile.dimensions['Time']), 'time steps were found in the input file')
                        
        for i in range(0,len(interpfieldlist)):
            
            interpfield = interpfieldlist[i]
            ncoutputfile = ncoutputfilelist[i]
            fieldunits = fieldunitslist[i]  
            interpoption = interppfieldlist[i]
            extrapfield = extrapfieldlist[i]

            corrfields=['pressure','pres','p','pressure_hpa','pres_hpa','p_hpa','z','ght','z_km','ght_km','tc','tk','theta','th','theta_e','thetae','eth']
            fieldtypes=['pressure','pres','p','pressure_hpa','pres_hpa','p_hpa','z','ght','z_km','ght_km','tc','tk','theta','th','theta-e','thetae','eth']
            if interpfield not in corrfields:
               fieldtype='none'
            else:
               fieldtype=fieldtypes[corrfields.index(interpfield)]
            
            print(fieldtype)
            print('Calculating ', interpfield, ' ...')
            timeidxs=range(len(ncfile.dimensions['Time']))
            for timestamp in timeidxs:
                print(round((timestamp/timeidxs[-1])*100), '%', end='\r')
                if fieldunits == None:
                   interpvar = getvar(ncfile, interpfield, timeidx=timestamp)
                else:
                   interpvar = getvar(ncfile, interpfield, timeidx=timestamp, units=fieldunits)
    
        
                if ('bottom_top' in interpvar.dims) == False:
                    plevelsinterpolatedfield = interpvar
                    if ('u_v' in interpvar.dims) == True:
                        plevelsinterpolatedfieldU = interpvar.isel(u_v=0)
                        plevelsinterpolatedfieldV = interpvar.isel(u_v=1)
                        plevelsinterpolatedfieldMOD = np.sqrt(plevelsinterpolatedfieldU*plevelsinterpolatedfieldU + plevelsinterpolatedfieldV*plevelsinterpolatedfieldV)
                    if interpoption==True:
                        if timestamp == 0:
                            print('Warning: interpolation is not an appliable method for single-level fields, and hence it will not be performed.')
                if ('bottom_top' in interpvar.dims) == True:
                    if interpoption==False:
                        plevelsinterpolatedfield = interpvar
                    if interpoption==True:
                        if timestamp == 0:
                            print('Interpolating ', interpfield,' to ', len(plevels), ' pressure levels ...')
                        if ('u_v' in interpvar.dims) == True:                           
                                plevelsinterpolatedfieldU = vinterp(ncfile, field=interpvar.isel(u_v=0), vert_coord="pressure", 
                                                               interp_levels=plevels, timeidx=timestamp,extrapolate=extrapfield)
                                plevelsinterpolatedfieldV = vinterp(ncfile, field=interpvar.isel(u_v=1), vert_coord="pressure", 
                                                               interp_levels=plevels, timeidx=timestamp,extrapolate=extrapfield)
                                plevelsinterpolatedfieldMOD= np.sqrt(plevelsinterpolatedfieldU*plevelsinterpolatedfieldU + plevelsinterpolatedfieldV*plevelsinterpolatedfieldV)                            
                        if ('u_v' in interpvar.dims) == False:
                            if interpfield=='z':
                               plevelsinterpolatedfield = vinterp(ncfile, field=interpvar, vert_coord="pressure", field_type='z',log_p=True,
                                                       interp_levels=plevels, timeidx=timestamp,extrapolate=extrapfield)
                            else:
                               plevelsinterpolatedfield = vinterp(ncfile, field=interpvar, vert_coord="pressure", field_type=fieldtype, log_p=True,  
                                                           interp_levels=plevels, timeidx=timestamp,extrapolate=extrapfield)
                        if timestamp == range(len(ncfile.dimensions['Time']))[-1]:
                            print('Interpolation of ', interpfield,' to pressure levels completed successfully')
                    
        
                #Export to netCDF:
                if ('u_v' in interpvar.dims) == False:
                    if timestamp == 0:
                        merged=plevelsinterpolatedfield
                    else:
                        merged=xarray.concat([merged,plevelsinterpolatedfield], 'Time')
                    
                    if timestamp == timeidxs[-1]:
                        del merged.attrs['coordinates']
                        merged.attrs['projection'] = str(merged.projection)
                        merged.XLONG.attrs['units'] = 'degrees_east'
                        merged.XLAT.attrs['units'] = 'degrees_north'
                        merged.to_netcdf(ncoutputfile) 
                        
                if ('u_v' in interpvar.dims) == True:
                    if timestamp == 0:
                        mergedU=plevelsinterpolatedfieldU
                        mergedV=plevelsinterpolatedfieldV
                        mergedMOD=plevelsinterpolatedfieldMOD
                    else:
                        mergedU=xarray.concat([mergedU,plevelsinterpolatedfieldU], 'Time')
                        mergedV=xarray.concat([mergedV,plevelsinterpolatedfieldV], 'Time')
                        mergedMOD=xarray.concat([mergedMOD,plevelsinterpolatedfieldMOD], 'Time')
                    
                    if timestamp == timeidxs[-1]:
                        ncoutputfileU = ncoutputfile.replace('.nc','') + '-U.nc'
                        del mergedU.attrs['coordinates']
                        mergedU.attrs['projection'] = str(mergedU.projection)
                        mergedU.XLONG.attrs['units'] = 'degrees_east'
                        mergedU.XLAT.attrs['units'] = 'degrees_north'
                        mergedU.to_netcdf(ncoutputfileU, mode='w') 
                        ncoutputfileV = ncoutputfile.replace('.nc','') + '-V.nc'
                        del mergedV.attrs['coordinates']
                        mergedV.attrs['projection'] = str(mergedV.projection)
                        mergedV.XLONG.attrs['units'] = 'degrees_east'
                        mergedV.XLAT.attrs['units'] = 'degrees_north'
                        mergedV.to_netcdf(ncoutputfileV, mode='w')
                        ncoutputfileMOD = ncoutputfile.replace('.nc','') + '-MOD.nc'
                        mergedMOD.XLONG.attrs['units'] = 'degrees_east'
                        mergedMOD.XLAT.attrs['units'] = 'degrees_north'
                        mergedMOD.to_netcdf(ncoutputfileMOD, mode='w')     
   

    print('Execution completed without any errors')
    
interpy()
