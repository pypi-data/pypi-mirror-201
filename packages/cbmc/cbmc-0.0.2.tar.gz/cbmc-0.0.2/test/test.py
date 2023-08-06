from cbmc import onpost
import cbmc

async def on_post(updated):
    print(f"有新的資料!!\n{updated}")
onpost(on_update=on_post)

#print(cbmc.get_post(222))