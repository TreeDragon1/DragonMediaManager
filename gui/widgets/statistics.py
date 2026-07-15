#################################################################
# STATISTICS
#################################################################

def build_statistics(self):

    stats = ctk.CTkFrame(
        self.main,
        fg_color="transparent"
    )

    stats.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=10,
        pady=(0, 15)
    )

    for i in range(5):
        stats.grid_columnconfigure(i, weight=1)

    self.movie_card = StatCard(
        stats,
        icon="🎬",
        title="Movies",
        value="0",
        subtitle="Total Movies"
    )

    self.tv_card = StatCard(
        stats,
        icon="📺",
        title="TV Shows",
        value="0",
        subtitle="Series"
    )

    self.episode_card = StatCard(
        stats,
        icon="🎞",
        title="Episodes",
        value="0",
        subtitle="Episodes"
    )

    self.download_card = StatCard(
        stats,
        icon="⬇",
        title="Downloads",
        value="0",
        subtitle="Active"
    )

    self.backup_card = StatCard(
        stats,
        icon="💾",
        title="Last Backup",
        value="--",
        subtitle="Status"
    )

    cards = [
        self.movie_card,
        self.tv_card,
        self.episode_card,
        self.download_card,
        self.backup_card
    ]

    for column, card in enumerate(cards):
        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="ew"
        )