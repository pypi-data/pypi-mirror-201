from faster_whisper.transcribe import Segment


class WordsToSegment:
    def __init__(self):
        self.pending_words = []
        self.max_words = 5

    def _get_words(self):
        while len(self.pending_words) > 0:
            yield self.pending_words.pop(0)

    def get_segments(self, segments):
        for segment in segments:
            yield self._get_segment(segment.words)

        while (pending := len(self.pending_words)) > 0:
            group_len = min(self.max_words, pending)
            yield self._get_segment(self.pending_words[0:group_len], False)

    def _get_segment(self, words, save=True):
        if save:
            self.pending_words += words

        counter = 0
        text = ""
        start = None
        end = None
        segment_words = []
        for word in self._get_words():
            #            print(f"{counter} - {word} - {pending}")
            text += word.word
            end = word.end
            segment_words.append(word)
            if counter == 0:
                start = word.start

            counter += 1

            if counter >= self.max_words:
                break

        return Segment(start, end, text, segment_words)
