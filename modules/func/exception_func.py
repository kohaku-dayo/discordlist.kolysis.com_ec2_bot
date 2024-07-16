import discord
sendLog = True

async def exception_process(response, succeedMessage:str, failedMessage:str):
    global sendLog
    try:
        response.raise_for_status()
    except Exception as e:
        if sendLog:
            print(f'[ERROR      ] {failedMessage}.......\n')
            print(f'Response Text -> {e.response.text}\n')
            print(f'Response Body -> {e.response}\n')
        return
    
    if sendLog:
        print(f'[INFO      ] {succeedMessage}\n')
