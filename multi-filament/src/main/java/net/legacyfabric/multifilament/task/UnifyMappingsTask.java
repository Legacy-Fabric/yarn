package net.legacyfabric.multifilament.task;

import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;
import net.fabricmc.mappingio.tree.MemoryMappingTree;

import net.legacyfabric.multifilament.mappingsio.FilteringMappingVisitor;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.tasks.InputDirectory;
import org.gradle.api.tasks.InputFile;

import javax.inject.Inject;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

public abstract class UnifyMappingsTask extends MappingOutputTask {
	@Inject
	public UnifyMappingsTask() {
		this.getOutputFormat().convention(MappingFormat.ENIGMA);
	}

	@InputDirectory
	public abstract DirectoryProperty getUnifiedDir();

	@InputDirectory
	public abstract DirectoryProperty getVersionedDir();

	void run(MappingWriter var1) throws IOException {
		this.getUnifiedDir().getAsFile().get().delete();
		Files.move(this.getOutputDir().getAsFile().get().toPath(), this.getUnifiedDir().getAsFile().get().toPath());
		MemoryMappingTree treeView = new MemoryMappingTree();
		MappingReader.read(this.getUnifiedDir().getAsFile().get().toPath(), treeView);
		MappingReader.read(this.getVersionedDir().getAsFile().get().toPath(), treeView);
		treeView.accept(var1);

		Files.walkFileTree(this.getUnifiedDir().getAsFile().get().toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});

		Files.walkFileTree(this.getVersionedDir().getAsFile().get().toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});
	}
}
