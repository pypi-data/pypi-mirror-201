from pylipd.lipd import LiPD

if __name__ == "__main__":
    lipd = LiPD()
    lipd.load_from_dir('/Users/varun/Downloads/example_sisal_lipds')

    query="""PREFIX le: <http://linked.earth/ontology#>
    PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    
    select ?dsname ?lat ?lon ?archive ?table ?varname ?varunits ?val ?timevarname ?timeunits ?timeval 
           ?depthvarname ?depthunits ?depthval 
           ?enstable ?ensvarname ?ensval ?ensunits ?ensdepthvarname ?ensdepthval ?ensdepthunits where {
        ?ds a le:Dataset .
        ?ds le:name ?dsname .
        
        ?ds le:collectedFrom ?loc . 
        ?loc wgs:lat ?lat .
        ?loc wgs:long ?lon .
        
        ?ds le:proxyArchiveType ?archive .
        	FILTER regex(?archive, "speleothem.*") .
            
        ?ds le:includesPaleoData ?data .
        ?data le:foundInMeasurementTable ?table .
        
        ?table le:includesVariable ?var .
        ?var le:name ?varname .
            FILTER regex(?varname, "d18O.*") .
        ?var le:hasValues ?val .
            OPTIONAL{?var le:hasUnits ?varunits } .
    
        ?table le:includesVariable ?timevar .
        ?timevar le:name ?timevarname .
            FILTER regex(?timevarname, "age.*").
        ?timevar le:hasValues ?timeval .
            OPTIONAL{?timevar le:hasUnits ?timeunits }
        
        OPTIONAL{?table le:includesVariable ?depthvar .
        ?depthvar le:name ?depthvarname .
            FILTER regex(?depthvarname, "depth.*").
        ?depthvar le:hasValues ?depthval .
            OPTIONAL{?depthvar le:hasUnits ?depthunits .}}
        
        ?ds le:includesChronData ?chron .
        ?chron le:chronModeledBy ?model .
        ?model le:foundInEnsembleTable ?enstable .
        
        ?enstable le:includesVariable ?ensvar .
        ?ensvar le:name ?ensvarname .
            FILTER regex(?ensvarname, "age.*").
        
        ?enstable le:includesVariable ?ensdepthvar .
        ?ensdepthvar le:name ?ensdepthvarname .
            FILTER regex(?ensdepthvarname, "depth.*").
        ?ensdepthvar le:hasValues ?ensdepthval .
            OPTIONAL{?ensdepthvar le:hasUnits ?ensdepthunits .}
        
    }
        """  
    
    result, result_df = lipd.query(query)
    print(result_df["varname"])