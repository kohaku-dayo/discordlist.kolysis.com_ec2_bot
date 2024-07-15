import discord
sendLog = True

async def exception_process(response, succeedMessage:str, failedMessage:str, followup:discord.Webhook = None):
    global sendLog
    try:
        response.raise_for_status()
    except Exception as e:
        if followup is not None:
            await followup.send(failedMessage)
        if sendLog:
            print(f'[ERROR      ] {failedMessage}.......\n')
            print(f'Response Text -> {e.response.text}\n')
            print(f'Response Body -> {e.response}\n')
        return
    
    if followup is not None:
            await followup.send(succeedMessage)
    if sendLog:
        print(f'[INFO      ] {succeedMessage}\n')
