from django.db import models

# Create your models here.
RANK_ORDER = {
    'Iron 1': 1, 'Iron 2': 2, 'Iron 3': 3,
    'Bronze 1': 4, 'Bronze 2': 5, 'Bronze 3': 6,
    'Silver 1': 7, 'Silver 2': 8, 'Silver 3': 9,
    'Gold 1': 10, 'Gold 2': 11, 'Gold 3': 12,
    'Platinum 1': 13, 'Platinum 2': 14, 'Platinum 3': 15,
    'Diamond 1': 16, 'Diamond 2': 17, 'Diamond 3': 18,
    'Ascendant 1': 19, 'Ascendant 2': 20, 'Ascendant 3': 21,
    'Immortal 1': 22, 'Immortal 2': 23, 'Immortal 3': 24,
    'Radiant': 25,
}

RANK_CHOICES = [(r, r) for r in RANK_ORDER.keys()]

class Agent(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Map(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Player(models.Model):
    REGION_CHOICES = [
        ('NA', 'North America'),
        ('EU', 'Europe'),
        ('AP', 'Asia Pacific'),
        ('KR', 'Korea'),
        ('BR', 'Brazil'),
        ('LATAM', 'Latin America'),
    ]

    username = models.CharField(max_length=50)
    current_rank = models.CharField(max_length=50, choices=RANK_CHOICES)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)

    def __str__(self):
        return self.username
    
class Match(models.Model):
    date = models.DateField(db_index=True)
    map = models.ForeignKey(Map, on_delete=models.SET_NULL, null=True, db_index=True)
    team_a_score = models.IntegerField()
    team_b_score = models.IntegerField()
    duration_minutes = models.IntegerField()
    avg_lobby_rank = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Match on {self.date} - {self.map} ({self.team_a_score}-{self.team_b_score})"

    class Meta:
        indexes = [
            models.Index(fields=['map', 'date']),
        ]

class MatchEntry(models.Model):
    TEAM_CHOICES = [('A', 'Team A'), ('B', 'Team B')]

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    team = models.CharField(max_length=1, choices=TEAM_CHOICES)
    rank_at_match = models.CharField(max_length=20, choices=RANK_CHOICES)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    @property
    def won(self):
        if self.team == 'A':
            return self.match.team_a_score > self.match.team_b_score
        return self.match.team_b_score > self.match.team_a_score
    
    def __str__(self):
        return f"{self.player} as {self.agent} in {self.match}"