import React from "react";
import styles from "./SummaryLayout.module.scss";
import {Desktop, Mobile} from "../../_hoc/Responsive";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";

const SummaryLayout = (props) => {
  const iconEl = (
    <>
      {props.icon}
      <Typography variant="subtitle1"
                  className={styles.IconText}>{props.iconText}</Typography>
    </>
  )

  return (
    <div className={styles.SummaryContainer}>
      <Desktop>
        <div className={styles.IconContainerDesktop}>
          {iconEl}
        </div>
      </Desktop>
      {/* eslint-disable-next-line react/jsx-no-undef */}
      <Mobile>
        <div className={styles.IconContainerMobile}>
          <div className={styles.HorizontalLine}/>
          <div className={styles.IconWrapper}>
            {iconEl}
          </div>
          <div className={styles.HorizontalLine}/>
        </div>
      </Mobile>
      <div className={styles.InfoContainer}>
        <div className={styles.FormContainer}>
          {props.formElement}
        </div>
        <div className={styles.Summary}>
          <Button onClick={props.onSubmit}
                  variant="contained">Update</Button>
          {props.summaryElement}
        </div>
      </div>
    </div>
  )
}

export default SummaryLayout;
