import datetime
import imaplib

m = imaplib.IMAP4_SSL("imap.gmail.com")  # server to connect to
print "Connecting to mailbox..."
m.login('mattaquiles@gmail.com', 'password')

print m.select('[Gmail]/All Mail')  # required to perform search, m.list() for all lables, '[Gmail]/Sent Mail'
before_date = (datetime.date(2016, 5, 1)).strftime("%d-%b-%Y")  # date string, 04-Jan-2013
typ, data = m.search(None, '(BEFORE {0})'.format(before_date))  # search pointer for msgs before before_date

if data != ['']:  # if not empty list means messages exist
    no_msgs = data[0].split()[-1]  # last msg id in the list
    print "To be removed:\t", no_msgs, "messages found with date before", before_date
    m.store("1:{0}".format(no_msgs), '+X-GM-LABELS', '\\Trash')  # move to trash
    print "Deleted {0} messages. Closing connection & logging out.".format(no_msgs)
else:
    print "Nothing to remove."

#This block empties trash, remove if you want to keep, Gmail auto purges trash after 30 days.
print("Emptying Trash & Expunge...")
m.select('[Gmail]/Trash')  # select all trash
m.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
m.expunge()  # not need if auto-expunge enabled

print("Done. Closing connection & logging out.")
m.close()
m.logout()
print "All Done."