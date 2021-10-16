from telethon.sync import TelegramClient,functions,types,events,errors
from telethon.tl.custom import Button
from time import sleep
import sys,requests,random,os,json,string,time
from lxml import html
#---------
bot = TelegramClient('when',2075333445,'AAFog0sJ1y_EyR19SVdnFq77NrhW1WU1VqA')
bot.start()
info = bot.get_me()
#---------alert
print(f'Bot Connected on {info.username}Successfully !')
#---------data's
admins = [1844001729]
w = bot.get_entity('@moneyprinters_admin')
admins.append(w.id)
data = dict()
usernames = []
#---------load_folders
for item in ['Accounts','Api','Database']:
    if not os.path.exists(item):
        os.mkdir(item)
#---------def's_functions
def gen():#def for create random password
    keywords = string.ascii_lowercase + string.ascii_uppercase + string.digits 
    return ''.join(random.choice(keywords) for i in range(random.randint(8,11)))
def get_file(pat):
    try:
        with open(f'Database/{pat}.txt','r') as fd:
            content = fd.readlines()
            fd.close()
            return content
    except FileNotFoundError:
        return 0
def get_api(phone):
    try:
        with open(f'Api/{phone}.txt','r') as fd:
            content = fd.read()
            fd.close()
            return [content.split(':')[0],content.split(':')[1]]
    except FileNotFoundError:
        return 0

def create_api(phone):
    body = 'phone={0}'.format(phone)
    try:
        response = requests.post('https://my.telegram.org/auth/send_password',data=body,headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
        s = json.loads(response.content)
        return s['random_hash']
    except:
        return False
def auth(phone,hash_code,pwd):
    data2 = "phone={0}&random_hash={1}&password={2}".format(phone,hash_code,pwd)
    responses = requests.post('https://my.telegram.org/auth/login',data=data2,headers= {"Origin":"https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "application/json, text/javascript, */*; q=0.01","Reffer": "https://my.telegram.org/auth","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
    try:
        return responses.cookies['stel_token']
    except:
        return False
def auth2(stel_token):
    resp = requests.get('https://my.telegram.org/apps',headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":"stel_token={0}".format(stel_token),"Cache-Control": "max-age=0",})
    tree = html.fromstring(resp.content)
    api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
    try:
        return '{0}:{1}'.format(api[0],api[1])
    except:
        s = resp.text.split('"/>')[0]
        value = s.split('<input type="hidden" name="hash" value="')[1]
        on = "hash={0}&app_title=Coded By Arash&app_shortname=Love Telegram&app_url=&app_platform=desktop&app_desc=".format(value)
        requests.post('https://my.telegram.org/apps/create',data=on,headers={"Cookie":"stel_token={0}".format(stel_token),"Origin": "https://my.telegram.org","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*","Referer": "https://my.telegram.org/apps","X-Requested-With": "XMLHttpRequest","Connection":"keep-alive","Dnt":"1",})
        respv = requests.get('https://my.telegram.org/apps',headers={"Dnt":"1","Accept-Encoding": "gzip, deflate, br","Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Reffer": "https://my.telegram.org/org","Cookie":"stel_token={0}".format(stel_token),"Cache-Control": "max-age=0",})
        trees = html.fromstring(respv.content)
        apis = trees.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
        return '{0}:{1}'.format(apis[0],apis[1])
async def worker(msg,link,delay):#phone,link,changer):
    ev = []
    accs = []
    tl = 1
    for item in os.scandir('Accounts'):
        if 'journal' not in item.name and '.session' in item.name:
            l = [[Button.inline(f'{tl} - {item.name}'),Button.inline('♻️')]]
            accs.append(item.name)
            ev.extend(l)
            tl+=1
    ev.extend([[Button.inline('Last Work '),Button.inline(time.ctime(time.time()))]])
    worker_msg = await msg.edit(f'Worker Launched with this informations\nTarget -> {link}\nAdd per account -> {delay}',buttons = ev)
    text = f'Log Sender Start in -> {time.ctime(time.time())}'
    log_msg = await msg.reply(text)
    for account in accs:
        rest = 0 
        success = 0
        another = 0
        w =  get_api(account.split('.session')[0])
        client = TelegramClient(f'Accounts/{account}',int(w[0]),w[1])
        await client.connect()
        async def join(clt,ls):
            try:
                if '@' in ls:
                    await clt(functions.channels.JoinChannelRequest(channel=ls))
                else:
                    await clt(functions.messages.ImportChatInviteRequest(hash=ls.split('/')[-1]))
                return True
            except errors.UserAlreadyParticipantError:
                return True 
            except errors.UserDeactivatedBanError:
                return -1
            except errors.UserDeactivatedError:
                return -1
            except errors.SessionExpiredError:
                return -2
            except errors.SessionRevokedError:
                return -2
        ww = await join(client,link)
        if ww == True:
            text += f'\nAccount {account} Joined Successfully ! {time.ctime(time.time())}'
            await log_msg.edit(text)
            for i in range(int(delay)):
                try:
                    await client(functions.channels.InviteToChannelRequest(channel=link,users=[usernames.pop()]))
                    success+=1
                    time.sleep(random.randint(5,10)/10)
                except IndexError:
                    text += f'\nProcess Completed ! **Username list is empty** {time.ctime(time.time())}'
                    try:
                        await log_msg.edit(text)
                    except Exception:
                        continue
                    break
                except errors.rpcerrorlist.UserPrivacyRestrictedError:
                    rest +=1
                    time.sleep(random.randint(5,10)/10)
                    print(2)
                    continue
                except errors.rpcerrorlist.PeerFloodError as t:
                    time.sleep(random.randint(1,10)/10)
                    '''
                    print(3)
                    tm = random.randint(60,120)
                    text += f'\nAccount {account} Flooded Sleep {tm} Seconds ... {time.ctime(time.time())}'
                    await log_msg.edit(text)
                    time.sleep(tm)
                    text += f'\nDone we wait for {tm} seconds now i continue... {time.ctime(time.time())} '
                    await log_msg.edit(text)
                    '''
                    continue
                except Exception as e :
                    print(4)
                    another +=1
                    print(e)
                    text += f'\nAccount {account} With unexcepted Error i skip this ... {time.ctime(time.time())} '
                    try:
                        await log_msg.edit(text)
                    except Exception:
                        continue
                    continue
            text += f'\nDone Account {account} End his work ! Total Locked Privacy **{rest}** Total success {success} Total Errors {another} {time.ctime(time.time())}'
            try:
                await log_msg.edit(text)
            except Exception:
                continue
            await client.disconnect()
        else:
            text += f'\nAccount {account} Cant Join! Error code {ww} ! {time.ctime(time.time())}'
            await client.disconnect()
    text += f'\nDone Process completed on {time.ctime(time.time())}'
    try:
        await log_msg.edit(text)
    except Exception:
        pass
    await msg.reply('Done Process End')
    await client.disconnect()




    
#---------
@bot.on(events.NewMessage)
async def my_event_handler(event):
    if event.sender_id in admins:
        if event.raw_text.lower().startswith('/login'):
            phones = event.raw_text.split('/login ')[1].replace(' ','')
            if os.path.exists('Accounts/{0}.session'.format(phones)):
                await event.reply('**Account Already In Database !**')
            else:
                await event.reply('**Please Wait...**')
                result = create_api(phones)
                if result == False:
                    await event.reply('**We Have Some Errors To Send Code For {} !**'.format(phones))
                else:
                    await event.reply('**Authunication Code Successfully Sended To {0}\nPlease Enter Code With This Format /auth CODE**'.format(event.raw_text.split('/login ')[1]))
                    data['auth_mode'] = '{0}:{1}'.format(phones,result)
        elif event.raw_text.lower().startswith('/auth'):
            try:
                key = data['auth_mode']
                await event.reply('**Please Wait ... **')
                result = auth(key.split(':')[0],key.split(':')[1],event.raw_text.split('/auth ')[1])
                if result == False:
                    await event.reply('**We Have Some Errors For Create Api Please Try Again Later ...**')
                    data.clear()
                else:
                    await event.reply('**Done Account Loginned Successfully Please Wait...**')
                    api_info = auth2(result)
                    await event.reply('**Done Api [{0}] Created Successfully !\nPlease Wait For Send Code...**'.format(api_info))
                    with open('Api/{0}.txt'.format(key.split(':')[0]),'w') as file:
                        file.write('{0}:{1}'.format(api_info.split(':')[0],api_info.split(':')[1]))
                        file.close()
                    data.clear()
                    new =  TelegramClient('Accounts/{0}'.format(key.split(':')[0]),int(api_info.split(':')[0]),api_info.split(':')[1])
                    await new.connect()
                    if not await new.is_user_authorized():
                        try:
                            result = await new.send_code_request(key.split(':')[0])
                            data['code_mode'] = '{0}:{1}:{2}:{3}'.format(key.split(':')[0],result.phone_code_hash,api_info.split(':')[0],api_info.split(':')[1])
                            await new.disconnect()
                            await event.reply('**Done Code Sended Please Enter Code With This Format /code CODE **')
                        except Exception:
                            await event.reply('**Error In Send Code Please Try Again Later...**')
            except KeyError:
                await event.reply('** No Any Account In Queue**')
        elif event.raw_text.lower().startswith('/code'):
            try:
                key = data['code_mode']
                await event.reply('**Please Wait ... **')
                new =  TelegramClient('Accounts/{0}'.format(key.split(':')[0]),int(key.split(':')[2]),key.split(':')[3])
                await new.connect()
                await new(functions.auth.SignInRequest(phone_number=key.split(':')[0],phone_code_hash=key.split(':')[1],phone_code=event.raw_text.split('/code ')[1]))
                await event.reply('**Done Account Loginned Successfully!**')
                data.clear()
            except errors.SessionPasswordNeededError:
                await event.reply('**Session Need Password Please Enter Password With This Format /step PASSWORD**')
                data.clear()
                data['step_mode'] = key
            except KeyError:
                await event.reply('** No Any Account In Queue**')
            await new.disconnect()
        elif event.raw_text.lower().startswith('/step'):
            try:
                key = data['step_mode']
                await event.reply('**Please Wait ... **')
                k2 = get_api(key.split(':')[0])
                new =  TelegramClient('Accounts/{0}'.format(key.split(':')[0]),int(k2[0]),k2[1])
                await new.connect()
                await new.sign_in(password=event.raw_text.split('/step ')[1])
                data.clear()
                info = await new.get_me()
                await new.disconnect()
                await event.reply('**Done Api [{0}] Successfully Added To Database !\nAccount Info\nAccount Username : {1}\nAccount Phone : +{2}\nAccount FirstName : {3}\nAccount LastName : {4}**'.format(key.split(':')[2]+':'+key.split(':')[3],str(info.username),str(info.phone),info.first_name,info.last_name))
            except KeyError:
                await event.reply('** No Any Account In Queue**')
            except errors.PasswordHashInvalidError:
                await event.reply('** Password Is Invalid Please Enter True Password With This Format /step PASSWORD**')
            await new.disconnect()
        elif event.raw_text.lower().startswith('leach'):
            link = event.raw_text.split('leach ')[1]
            if 'joinchat' in link:
                link = link.split('/')[-1]
            if '@' in event.raw_text or 'joinchat' in event.raw_text:
                ev = []
                for item in os.scandir('Accounts'):
                    if 'journal' not in item.name and '.session' in item.name:
                        l = [[Button.inline(item.name,f'leach|{item.name}|{link}')]]
                        ev.extend(l)
                await event.reply(f'OK Please select one account for leach from\nhttps://t.me/joinchat/{link}',buttons=ev)
            else:
                await event.reply('Please Enter Link With True Format!\n🆘https://t.me/joinchat/example\n🆘@group')
        elif event.raw_text.lower() == 'accounts':
            ev = []
            tl = 0 
            for item in os.scandir('Accounts'):
                if 'journal' not in item.name and '.session' in item.name:
                    l = [[Button.inline(item.name,f'settings|{item.name}')]]
                    ev.extend(l)
                    tl +=1
            if tl >= 1:
                await event.reply(f'You Can See All {tl} Accounts Here',buttons=ev)
            else:
                await event.reply('Database Is Empty!')
        elif event.raw_text.lower().startswith('load'):
            my = event.raw_text.split('load ')[1]
            if my == 'all':
                ev = []
                for item in os.scandir('Database'):
                    l = [[Button.inline(item.name,f'load|{item.name}')]]
                    ev.extend(l)
                if len(l) >= 1 :
                    await event.reply('You Can See All lists you can load list by click ',buttons=ev)
                else:
                    await event.reply('List Is Empty!')
            else:
                w = get_file(my)
                if w != 0:
                    for item in w:
                        usernames.append(item.split('\n')[0])
                    await event.reply(f'Done Total {len(usernames)} Loaded Successfully!')
                else:
                    await event.reply('Wrong File name use load all to see files')
        elif event.raw_text.lower() == 'clear':
            if len(usernames) != 0:
                await event.reply(f'Are You Sure You Want To Delete {len(usernames)} ?' , buttons = [
                    [Button.inline('Yes','clean'),Button.inline('No','no')],
                ])
            else:
                await event.reply('Usernames Is Empty!')
        elif event.raw_text.lower() == 'info':
            await event.reply(f'Total Usernames : {len(usernames)}')
        elif event.raw_text.lower() == 'ping':
            await event.reply('Im Online !')
        elif event.raw_text.lower().startswith('add'):
            #add @group 20 all
            datas = event.raw_text.split(' ')
            if 'joinchat' in datas[1] :
                link = datas[1]
            elif '@' in datas[1]:
                link = datas[1]
            else:
                link = None
            if link != None:
                msg = await event.reply('Please wait ...')
                await worker(msg,datas[1],datas[2])
            else:
                await event.reply('Target group information is incorrect!')
        elif event.raw_text.lower() == 'help':
            await event.reply('➖➖➖➖➖➖➖➖\nhelp\n\n**For Show Help Message **\n➖➖➖➖➖➖➖➖\n/login `Phone Number`\n\n**For Login New Account **\n➖➖➖➖➖➖➖➖\n/auth `CODE`\n\n**For Verify Web Login**\n➖➖➖➖➖➖➖➖\n/code `CODE`\n\n**For Login With Code**\n➖➖➖➖➖➖➖➖\n/step `PASSWORD`\n\n**For Login With 2FA Password\n➖➖➖➖➖➖➖➖\nleach `@group` `t.me/joinchat/t…`\n\n** For Leach Users From Target Group\n➖➖➖➖➖➖➖➖\naccounts\n\n**For Show Delete or sort accounts**\n➖➖➖➖➖➖➖➖\nload `File Name` `all`\n\n**Load File name load your target file**\n**Load all load all lists and show you**\n➖➖➖➖➖➖➖➖\ninfo \n\n**For See How Much usernames Loaded**\n➖➖➖➖➖➖➖➖\nping\n\n**For Check bot status**\n➖➖➖➖➖➖➖➖\nadd `link` `number`\n\n**Add users to group link starts with @ or t.me/joinchat/ **\n**Pay Attention Max Number is 50**\n➖➖➖➖➖➖➖➖\nTelegram User Scraper/Adder ')
@bot.on(events.CallbackQuery)
async def evt(events):
    callback = events.data.decode()
    if callback.startswith('leach'):
        phone , link = callback.split('|')[1] , callback.split('|')[2]
        await events.answer('Please wait ...')
        sleep(0.5)
        await events.edit(f'Trying To Connect {phone}...')
        apis = get_api(phone.split('.session')[0])
        sleep(0.5)
        async def join(client,link):
            try:
                if '@' in link:
                    await client(functions.channels.JoinChannelRequest(channel=link))
                else:
                    await client(functions.messages.ImportChatInviteRequest(hash=link))
                return True
            except errors.UserAlreadyParticipantError:
                return True 
            except errors.UserDeactivatedBanError:
                return -1
            except errors.UserDeactivatedError:
                return -1
            except errors.SessionExpiredError:
                return -2
            except errors.SessionRevokedError:
                return -2
        if apis != 0:
            await events.edit(f"Api_id And Api_hash Loaded Successfully Please Wait...")
            client = TelegramClient(f'Accounts/{phone}',int(apis[0]),apis[1])
            await client.connect()
            ww = await join(client,link)
            if ww == True:
                await events.edit('Account Joined Successfully Please wait ...')
                if '@' in link:
                    keu = link.split('@')[1]
                elif 'joinchat' in link:
                    keu = link.split('/')[-1]
                fl = open(f'Database/{keu}.txt','w')
                i = 0
                if not '@' in link:
                    link = f'https://t.me/joinchat/{link}'
                async for item in client.iter_participants(link):
                    if item.username != None:
                        fl.write(item.username + '\n')
                        i+=1
                fl.close()
                await events.edit(f'Done ! Total {i} Members Leached ! Please wait for file ...')
                await bot.send_file(events.chat_id, f'Database/{keu}.txt', caption=f"Total {i} Leached Users.\nYou Can Load This Users with command load {keu}\nYou can see all lists with load all")    
                await client.disconnect()            
            elif ww == -1:
                await events.edit('Your account has been deleted ! ...')
                await client.disconnect()
            elif ww == -2:
                await events.edit('Sorry Bot kicked out from sessions ...')
                await client.disconnect()
        else:
            await events.edit(f'Error In find api data for account {phone}! Please Re Login this account!')
    elif callback == 'clean':
        usernames.clear()
        await events.edit('Done Usernames List is empty now!')
    elif callback == 'no':
        await events.edit('Ok i cancel this process')
    elif callback.startswith('load'):
        kuy = callback.split('|')[1]
        mfile = get_file(kuy.split('.txt')[0])
        if mfile != 0 :
            for item in mfile:
                usernames.append(item.split('\n')[0])
            await events.edit('Done')
        else:
            await events.edit('Sorry i cant load file ...')
    elif callback.startswith('settings'):
        phn = callback.split('|')[1]
        await events.reply(f'What you want with {phn} ?',buttons = [
            [Button.inline('Delete',f'delete|{phn}'),Button.inline('Close Panel','close')]
        ])
    elif callback == 'close':
        await events.edit('Panel Closed Successfully!')
    elif callback.startswith('delete'):
        pehen = callback.split('|')[1]
        try:
            os.remove(f'Accounts/{pehen}')
            await events.edit(f'Done Account {pehen} Successfully Removed From Database!')
        except :
            await events.edit(f'I cant delete {pehen} From database ! Try Again later...')








bot.run_until_disconnected()
