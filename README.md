# tv_notifier
Notification for TV series (For Ubantu)

# Create your own cron
nano series_notify.cron

Edit series_notify.cron (already included in the source)
--------------------------------------------------------
 * * * * * DISPLAY=:0.0 /home/webwerks/series_notify.py

To run the cron in ubantu
--------------------------------------------------------
crontab series_notify.cron
