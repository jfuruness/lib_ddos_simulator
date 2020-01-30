from copy import deepcopy
from random import shuffle

class User:
    """Bob"""
  
    def __init__(self, num: int, suspicion: float = 0, bucket = None):
        """Stores user values"""
    
        self.num = num
        self.suspicion = suspicion
        self.bucket = bucket

    def __eq__(self, other):
        if isinstance(other, User):
            return self.suspicion < other.suspicion

    def __repr__(self):
        return "User " + str(self.num)


class Attacker(User):
    """Mal"""
  
    def attack(self):
        pass

  
class Bucket:
    """Bucket has users (alice)"""
  
    def __init__(self, users: list = [], max_users=10000000):
        """Stores users"""
    
        self.users = []
        self._max_users = max_users
        self.contains_attacker = False

        for user in users:
            self.add_user(user)

    def __str__(self):
        return self.users
    
    def __len__(self):
        """Length of bucket"""
    
        return len(self.users)
    
    def add_user(self, user):
        """Adds a user, returns True if added else False"""
    
        if len(self.users) > self._max_users:
            return False
        else:
            self.users.append(user)
            if isinstance(user, Attacker):
                self.contains_attacker = True
            return True
    
    def update_sus(self):
        """Updates suspicion for all users in bucket"""
    
        if self.contains_attacker:
            # TODO: Custom iterator here
            for user in self.users:
                # TODO: figure out what val to add here
                user.suspicion += 1 / len(self.users)
    

    
class Simulation:
    """Can run a sim"""

    def __init__(self, num_good_users, num_attackers, threshold, num_buckets):
        """Saves parameters for the simulation"""

        self.manager = Manager(num_buckets, threshold)
        self.good_users = [User(x) for x in range(num_good_users)]
        self.attackers = [Attacker(x) for x in range(num_attackers)]
        self.users = self.good_users + self.attackers
        for user in self.users:
            self.manager.add_user(user)

    def run(self, num_rounds):
        # Goal is to provide as much service as possible
        # Keep as many users as you can, get rid of as many attackers as you can (asap)
        for turn in range(num_rounds):
            self.manager.detect(turn)
            self.manager.sieve_shuffle()
      



class Sieve_Sim(Simulation):
    """Runs seive sim"""

    def __init__(self, num_good_users, num_attackers, threshold, num_buckets):
    
        # Initializes Parent class
        super(Sieve_Sim, self).__init__(num_good_users, num_attackers,
                                        threshold, num_buckets)
      
class Manager:
    """Controls all buckets (Eve)"""
  
    def __init__(self, num_buckets: int, threshold: int):
        self.buckets = [Bucket() for _ in range(num_buckets)]
        # Doesn't matter because will just circle back to first bucket
        self._next_bucket = 0
        self.users = []
        self.threshold = threshold
    
    def add_user(self, user: User): 
        self.users.append(user)

        # WALRUS???
        self._next_bucket += 1
        if self._next_bucket >= len(self.buckets):
            self._next_bucket = 0
        if not self.buckets[self._next_bucket].add_user(user):
            for bucket in self.buckets:
                bucket.add_user(user)
                # If succeeds exit loop
                return
            # If you've reached this point, user does not fit into any bucket
            # So we need to decide whether to leave user out or buy a new bucket
            # if we buy a new bucket we must load balance
            # Impliment later
            1/0
    
    def sieve_shuffle(self):
        # TODO: Problem exists when buckets don't divide evenly,
        # It gets rid of a bucket
        user_chunks = []
        # Update suspicion
        self._update_sus()
        # https://stackoverflow.com/a/312464
        # NOTE: rounds down, could be a prob
        for i in range(0, len(self.users), len(self.buckets) // 2):
            # User chunk is the chunk Anna described
            user_chunks.append(deepcopy(self.users[i: i + len(self.buckets) // 2]))

        self.buckets = []
        # Splits user chunk randomly into two groups
        for user_chunk in user_chunks:
            shuffle(user_chunk)
            # adds a new bucket with half the users of that chunk randomly
            self.buckets.append(Bucket(user_chunk[:len(user_chunk) // 2]))
            # adds a new bucket with half the users of that chunk randomly
            self.buckets.append(Bucket(user_chunk[len(user_chunk) // 2:]))
        # Flattens a list of user chunks into self.users
        self.users = [user for user_chunk in user_chunks for user in user_chunk]


    def detect(self, turn_num: int):
        users_to_remove = [user for user in self.users if user.suspicion > self.threshold]

        # TODO: Optimize later, prob should be dict? or set? not sure
        for user in users_to_remove:
            self.users.remove(user)
            if isinstance(user, Attacker):
                print("Discovered Attacker correctly on turn {}".format(turn_num))
                # TODO: should remove attacker here
            else:
                print("Discovered Attacker incorrectly on turn {}".format(turn_num))
                    

    def _update_sus(self):
        """Updates suspicion level of all users"""

        for bucket in self.buckets:
            bucket.update_sus()
        



if __name__ == "__main__":
    Sieve_Sim(num_good_users=100, num_attackers=10,
              threshold=10, num_buckets=4).run(num_rounds=50)
