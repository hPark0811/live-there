import React, {useState} from 'react';
import styles from './about-us.module.scss';
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Avatar from "@material-ui/core/Avatar";
import {makeStyles} from "@material-ui/core/styles";
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import {Desktop, Mobile} from "../../components/_hoc/Responsive";

const useStyles = makeStyles((theme) => ({
  largeProfileImageDesktop: {
    width: theme.spacing(26),
    height: theme.spacing(30),
    marginRight: theme.spacing(4)
  },
  largeProfileImageMobile: {
    width: theme.spacing(26),
    height: theme.spacing(30),
    margin: 'auto'
  },
  inlineIcon: {
    height: theme.spacing(2),
  }
}));

// TODO: Store these info in DB, so deployment is not needed everytime
const contributors = [
  {
    "name": "Heung Soo Park",
    "role": "Developer",
    "imageSrc": "heung.jpg",
    "contacts": {
      "email": "hpark0811@gmail.com",
      "linkedIn": "https://www.linkedin.com/in/heung-soo-park-87b0a7b5/",
      "github": "https://github.com/hPark0811"
    }
  },
  {
    "name": "Jeong Won Song",
    "role": "Developer",
    "imageSrc": "jeongwon.jpeg",
    "contacts": {
      "email": "jsong336@uwo.ca",
      "linkedIn": "https://www.linkedin.com/in/jeongwonsong/",
      "github": "https://github.com/jsong336"
    }
  },
  {
    "name": "Sami Nouralla",
    "role": "Developer",
    "imageSrc": "sami.jpeg",
    "contacts": {
      "email": "nourallasami@gmail.com",
      "linkedIn": "https://www.linkedin.com/in/sami-nouralla-a67382136/",
      "github": "https://github.com/snourall123"
    }
  },
  {
    "name": "Reina Song",
    "role": "Designer",
    "imageSrc": "reyna.png",
    "contacts": {
      "email": "r_song99740@fanshaweonline.ca",
      "linkedIn": "https://www.linkedin.com/in/reina-seungyeon/",
    }
  }
]

const AboutUs = () => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const [selectedContributor, setSelectedContributor] = useState(null);

  const handleClickOpen = (contributor) => {
    setSelectedContributor(contributor);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <div className={styles.topContainer}>
        <div className={styles.infoContainer}>
          <div className={styles.headerWrapper}>
            <Typography variant="h3"
                        component="h3"
                        className={styles.header}>
              Meet the Team
            </Typography>
          </div>
          <p>
            We are a group of engineers/designers who has a passion for learning new technologies and applying them to
            make people's life easier and bridge the gap between people's needs and wants. Please scroll below to know
            more about us!
          </p>
          <Button className={styles.contactUsBtn}
                  variant="outlined"
                  size="large"
                  target="_blank"
                  href="https://github.com/hPark0811/live-there">
            CONTRIBUTE
          </Button>
        </div>
      </div>
      <div className={styles.contributorsContainer}>
        {
          contributors.map((contributor, ndx) => {
            const images = require.context('../../assets', true);
            contributor.image = images('./' + contributor.imageSrc);
            return (
              <div className={styles.contributorWrapper}
                   key={ndx}
                   onClick={() => handleClickOpen(contributor)}>
                <Avatar alt={contributor.name}
                        src={contributor.image}
                        className={styles.contributorImg}/>
                <div>
                  <div><b>{contributor.name}</b></div>
                  <div>{contributor.role}</div>
                </div>
              </div>
            )
          })
        }
      </div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        {
          selectedContributor && <DialogContent>
            <div className={styles.dialogProfileContainer}>
              <Desktop>
                <Avatar variant="rounded"
                        className={classes.largeProfileImageDesktop}
                        src={selectedContributor.image}/>
              </Desktop>
              <Mobile>
                <Avatar variant="rounded"
                        className={classes.largeProfileImageMobile}
                        src={selectedContributor.image}/>
              </Mobile>
              <div>
                <p><b>{`${selectedContributor.name} - ${selectedContributor.role}`}</b></p>
                <p><b>E-mail: </b>{selectedContributor?.contacts?.email}</p>
                <p>
                  <b>LinkedIn: </b>
                  <a href={selectedContributor?.contacts?.linkedIn}
                     target="_blank">
                    visit profile
                  </a>
                </p>
                {selectedContributor?.contacts?.github && <p>
                  <b>Github: </b>
                  <a href={selectedContributor.contacts.github}
                     target="_blank">
                    visit profile
                  </a>
                </p>}
              </div>
            </div>
          </DialogContent>
        }
      </Dialog>
    </>
  )
}

export default AboutUs;
