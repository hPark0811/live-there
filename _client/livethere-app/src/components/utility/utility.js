import React, { useState } from 'react';
import axios from 'axios'
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';
import { FormControl, FormControlLabel, FormLabel, FormGroup, Checkbox } from '@material-ui/core';
import './utility.scss';

export const fetchUtilityFee = (universityId) => {
    // TODO: hide api end point
    return axios.get(`http://localhost:5000/utility?universityId=${universityId}`).then(response => {
        return response;
    }).catch(err => {
        console.log(err);
    });
}

const Utility = (props) => {
    const [includeEC, setIncludeEC] = useState(true);
    const [includeNG, setIncludeNG] = useState(true);

    let totalFee = 0;
    if (includeEC === true){
        totalFee += props.utilityData !== null ? props.utilityData.averageEC : 0;
    }
    if (includeNG === true){
        totalFee += props.utilityData !== null ? props.utilityData.averageNG : 0;
    }

    return props.utilityData === null ? null :
        <div className='utilityContainer'>
            <div className='imgContainer'>
                <AttachMoneyIcon fontSize='large'/>
            </div>
            <div className='overviewContainer'>
                <div className='formContainer'>
                    <FormControl>
                        <h3>Includes: </h3>
                        <FormGroup>
                            <FormControlLabel
                                control={<Checkbox checked={includeEC}/>}
                                labelPlacement='start'
                                onChange={() => setIncludeEC(prev=>!prev)}
                                label="Average Electricity"
                            />
                            <FormControlLabel
                                control={<Checkbox checked={includeNG}/>}
                                labelPlacement='start'
                                onChange={() => setIncludeNG(prev=>!prev)}
                                label="Average Natural Gas"
                            />
                        </FormGroup>
                    </FormControl>
                </div>
                <div className='infoContainer'>
                    Estimated total utility fees is in city of <b>{props.locationData.city}, {props.locationData.province}</b> is
                        = <b>${ totalFee }</b>
                </div>
            </div>
        </div>
}

export default Utility;

