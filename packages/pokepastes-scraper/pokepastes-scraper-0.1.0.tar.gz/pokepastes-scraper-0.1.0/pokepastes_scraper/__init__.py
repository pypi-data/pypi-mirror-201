
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
import os, itertools as it
from dataclasses import dataclass


__all__ = [
    "team_from_url"
]


@dataclass
class Stats:
    HP: int
    Atk: int
    Def: int
    SpA: int
    SpD: int
    Spe: int

    # e.g. stat_string = "4 Atk"
    def add_from_str(self, stat_string):
        val, stat = stat_string.split(' ')
        val = int(val)
        setattr(self, stat, val)



def EVs(HP=0, Atk=0, Def=0, SpA=0, SpD=0, Spe=0):
    return Stats(HP, Atk, Def, SpA, SpD, Spe)


def IVs(HP=31, Atk=31, Def=31, SpA=31, SpD=31, Spe=31):
    return Stats(HP, Atk, Def, SpA, SpD, Spe)


# https://pokepast.es/syntax.html 
# https://github.com/smogon/pokemon-showdown-client/blob/master/js/storage.js#L1291 ()
@dataclass
class PokepastesMon:
    # this should be the order they appear on the team's webpage
    # `None` should mean "unspecified"
    species: str = None
    nickname: str = None
    gender: str = None
    item: str = None
    ability: str = None
    level: int = None
    shiny: bool = None
    happiness: int = None
    pokeball: str = None
    # hidden_power_type: str = None # unnecessary?
    dynamax_level: int = None
    gigantamax: bool = None
    tera_type: str = None
    evs: Stats = None
    nature: str = None
    ivs: Stats = None
    moveset: list[str] = None

    @staticmethod
    def _from_pre(tag: Tag):
        # rule of thumb for this function: n = next(tags_iter) whenever you are done with n's current value
        tags_iter = iter(tag.children)
        res = PokepastesMon('asdfasdf')

        firstline = ''
        while True:
            n = next(tags_iter)
            firstline += n.text

            if '\n' in n.text:
                n = next(tags_iter)
                break

        if '@' in firstline:
            firstline, res.item = [s.strip() for s in firstline.split(' @ ')]
        
        # splits into "Nick", "Species)", "Gender)"
        parts = firstline.split(' (')

        if len(parts) == 1:
            res.species = firstline
        else:
            if parts[-1][1] in 'FM':
                res.gender = parts.pop()[1]
            
            if len(parts) == 1:
                res.species = parts[0]
            else:
                res.nickname = parts[0]
                # [1:-1] trims closing parentheses that we haven't trimmed yet
                res.species = parts[1][:-1]

        # if n.text.endswith('('):
        #     # three cases:
        #     # 1 Species (Gender) @
        #     # 2 Nick (Species) (Gender) @
        #     # 3 Nick (Species) @
        #     species_or_nick = n.text[:-2]

        #     n = next(tags_iter)
        #     if n.text in 'FM':
        #         # case 1
        #         res.species = species_or_nick
        #         res.gender = n.text
        #         n = next(tags_iter)
        #     else:
        #         res.nickname = species_or_nick
        #         res.species = n.text
        #         n = next(tags_iter)
        #         if n.text == ') (':
        #             n = next(tags_iter)
        #             assert(n.text in 'FM')
        #             res.gender = n.text
        #             n = next(tags_iter)
            
        #     # at this point, n.text == ')\n' or ') @ Item\n' 
        #     if n.text.strip() != ')':
        #         res.item = n.text[4:].strip()
        #     n = next(tags_iter)

        # else:
        #     # n.text == 'Species\n' or 'Species @ Item\n'
        #     res.species, res.item = [s.strip() for s in n.text.split('@')]
        #     n = next(tags_iter)


        # iterate through everything before moveset:
        while True:
            curr = n.text.strip()
            match curr:
                # ability: str = None
                # level: int = None
                # shiny: bool = None
                # happiness: int = None
                # pokeball: str = None
                # dynamax_level: int = None
                # gigantamax: bool = None
                # tera_type: str = None
                # evs: Stats = None
                # nature: str = None
                # ivs: Stats = None
                case 'Ability:':
                    n = next(tags_iter)
                    res.ability = n.text.strip()
                case 'Level:':
                    n = next(tags_iter)
                    res.level = int(n.text)
                case 'Shiny:':
                    n = next(tags_iter)
                    res.shiny = True
                case 'Happiness:':
                    n = next(tags_iter)
                    res.happiness = n.text.strip()
                case 'Pokeball:':
                    n = next(tags_iter)
                    res.pokeball = n.text.strip()
                case 'Dynamax Level:':
                    n = next(tags_iter)
                    res.dynamax_level = n.text.strip()
                case 'Gigantamax:':
                    n = next(tags_iter)
                    res.gigantamax = True
                case 'Tera Type:':
                    n = next(tags_iter)
                    res.tera_type = n.text.strip()
                # see below match statement for evs: ivs: case
                case '-':
                    break
                case other:
                    if other.strip().endswith('Nature'):
                        res.nature, _ = other.split(' ')    

            if curr and curr in 'EVs:IVs:':
                if curr == 'IVs':
                    stats = IVs()
                    res.ivs = stats
                else:
                    stats = EVs()
                    res.evs = stats
                
                while True:
                    n = next(tags_iter)
                    stats.add_from_str(n.text.strip())
                    
                    n = next(tags_iter)
                    if n.text != ' / ':
                        break
            
            else:
                n = next(tags_iter)
        
    
        # n is on a '-' before the first move
        res.moveset = []

        # skip '-'
        n = next(tags_iter)

        for _ in range(3):
            res.moveset.append(n.text.strip())
            n = next(tags_iter)
            # skip '-'
            n = next(tags_iter)

        # don't `n = next(tags_iter)` on the last iteration to not raise StopIteration
        res.moveset.append(n.text.strip())
        return res


@dataclass
class PokepastesTeam:
    members: list[PokepastesMon] = None

    title: str = None
    author: str = None
    desc: str = None


def team_from_url(url: str):
    page = requests.get(url)
    return team_from_html(page.text)


def team_from_html(text: str):
    res = PokepastesTeam()
    soup = BeautifulSoup(text, 'html.parser')

    sidebar: Tag = soup.find('aside')
    sidebar_iter = iter(sidebar.children)

    # get first six elements, and save three meaningful ones
    _, res.title, _, author_line, _, res.desc = \
        [i.text.strip() for i in it.islice(sidebar_iter, 6)]

    # get stuff right of first 'by' (there must be a better way)
    res.author = ''.join(author_line.split('by')[1:]).strip()

    html_mons = soup.find_all('pre')    
    res.members = [PokepastesMon._from_pre(mon) for mon in html_mons]

    return res