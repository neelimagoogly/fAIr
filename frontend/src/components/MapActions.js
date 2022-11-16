import React, { useState } from 'react'
import LoadingButton from "@mui/lab/LoadingButton";

import ImportExportIcon from '@mui/icons-material/ImportExport';
import axios from '../axios'
import { useMutation } from 'react-query';
import { Grid } from '@mui/material';

const MapActions = props =>
{

    const [error, setError] = useState(false)
    const downloadDS = async () =>
    {

        try {
           
            const body = 
            {
                dataset_id: 1,
                source: props.oamImagery.url,
                zoom_level: [19,20]
            }
            setError(false)
            const res = await axios.post("/dataset_image/build/",body);
      
            console.log(res)
            if (res.error) {
                    setError(res.error.response.data.Error);
                    return;
                }

            return res.data;
          } catch (e) {
            console.log("isError");
            setError(e);
          } finally {
          
          }
    }

    const { mutate, data, isLoading } = useMutation(downloadDS);

    return <>
    {/* { JSON.stringify(props.oamImagery) } */}
    {/* <br/> */}
    <Grid item xs={12} md={12} paddingTop={1}>     
     <LoadingButton
              onClick={(e)=>{ console.log("Build") ; mutate() }}
              endIcon={<ImportExportIcon  />}
              loading={isLoading}
              loadingPosition="end"
              variant="contained"
              disabled={props.oamImagery === null}
            >
              Sync Dataset
            </LoadingButton>
            <br/>
            {error && error}
            </Grid>
      </>
        

}
export default MapActions;