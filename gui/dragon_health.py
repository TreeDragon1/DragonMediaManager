"""
Dragon Media Manager
Dragon Health Panel

Version: v0.1.3-alpha
Build 8.5.3
"""

import customtkinter as ctk
from core.dragon_health import DragonHealthCore

class DragonHealth(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(corner_radius=12)
        self.health=DragonHealthCore().get_health()

        ctk.CTkLabel(self,text="🐉 Dragon Health",font=("Arial",22,"bold")).pack(anchor="w",padx=20,pady=(15,10))

        for service,status in self.health.get("services",{}).items():
            self.create_row(service,status)

        self.separator()
        self.create_row("💾 Movies Drive",self.health.get("movies","--"))
        self.create_row("🧠 Memory",self.health.get("memory","--"))
        self.separator()

        ctk.CTkLabel(self,text="Dragon Status",font=("Arial",18,"bold")).pack()

        status=self.health.get("status","Excellent")
        colour="lime green" if "Excellent" in status else ("orange" if "Good" in status else "red")
        ctk.CTkLabel(self,text=status.replace("🟢 ","").replace("🟡 ","").replace("🔴 ",""),
                     text_color=colour,font=("Arial",20,"bold")).pack(pady=(0,10))

        ctk.CTkLabel(self,text=f"Dragon Score: {self.health.get('score',0)}%",
                     font=("Arial",18,"bold")).pack(pady=(0,20))

    def separator(self):
        ctk.CTkLabel(self,text="─"*30).pack(fill="x",padx=20,pady=10)

    def create_row(self,title,value):
        row=ctk.CTkFrame(self,fg_color="transparent")
        row.pack(fill="x",padx=20,pady=4)

        ctk.CTkLabel(row,text=title,font=("Arial",15)).pack(side="left")

        clean=value.replace("🟢 ","").replace("🔴 ","").replace("🟡 ","")
        if "Online" in value or "Running" in value:
            colour="lime green"
        elif "Offline" in value:
            colour="red"
        else:
            colour="orange"

        ctk.CTkLabel(row,text=clean,text_color=colour,font=("Arial",15,"bold")).pack(side="right")
